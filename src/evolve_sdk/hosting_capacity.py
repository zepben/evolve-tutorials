#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import asyncio
import json
from functools import reduce
from math import ceil
from random import choice
from typing import Tuple, Callable, Set, List

import pandapower as pp
from pandapower import control
from pp_creators.creator_ee import PandaPowerNetworkCreatorEE
from zepben.eas import EasClient
from zepben.evolve import NetworkConsumerClient, NetworkService, Feeder, PhaseCode, EnergySource, Terminal, \
    connect_async, Dict, ConductingEquipment, PowerTransformer, PowerElectronicsConnection, \
    PerLengthSequenceImpedance, OverheadWireInfo, AcLineSegment, \
    EnergyConsumer, BusBranchNetworkCreationMappings

from utils.ev_hosting_capacity_study_creator import upload_ev_charging_study
from utils.tracing import get_downstream_eq
from utils.utils import get_logger, read_json_config


class DistTransformerInfo:
    def __init__(self, bus_idx: int, customer_count: int, name: str):
        self.bus_idx = bus_idx
        self.customer_count = customer_count
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, DistTransformerInfo):
            return False

        return other.bus_idx == self.bus_idx

    def __hash__(self):
        return self.bus_idx


async def hosting_capacity():
    logger = get_logger()
    auth_config = read_json_config("../auth_config_files\\auth_config.json")
    study_args = read_json_config("../src\\evolve_sdk\\study_args_hosting_capacity.json")
    async with connect_async(
            host=auth_config["ewb_server"]["host"],
            rpc_port=auth_config["ewb_server"]["rpc_port"],
            conf_address=auth_config["auth0"]["conf_address"],
            client_id=auth_config["auth0"]["client_id"],
            username=auth_config["auth0"]["username"],
            password=auth_config["auth0"]["password"],
            secure=True
    ) as channel:
        feeder_mrid = study_args["feeder"]
        print(f"Fetching Feeder {feeder_mrid} ...")
        network = await _get_feeder_network(channel, feeder_mrid)
        load_provider, pec_load_provider = await get_load_providers(network, study_args)
        print(f"Fetched Feeder")

        print(f"Creating Pandapower model ...")
        creator = PandaPowerNetworkCreatorEE(
            vm_pu=1.0,
            load_provider=load_provider,
            pec_load_provider=pec_load_provider,
            logger=logger
        )
        result = await creator.create(_remove_lv(network))
        print(f"Created Pandapower model")

        if result.was_successful:
            pp_initial_net = _add_regulator_controllers(result.network)
            diagnostic = pp.diagnostic(pp_initial_net, report_style=None)
            if len(diagnostic) == 0:
                eas_client = EasClient(
                    host=auth_config["eas_server"]["host"],
                    port=auth_config["eas_server"]["port"],
                    client_id=auth_config["eas_server"]["client_id"],
                    username=auth_config["eas_server"]["username"],
                    password=auth_config["eas_server"]["password"]
                )

                ev_p_w = study_args["ev_charging"]["ev_p_w"]
                ev_q_var = study_args["ev_charging"]["ev_q_var"]
                for ev_penetration in study_args["ev_charging"]["penetration_percents"]:
                    print("\n\n---------------------------------------")
                    added_ev_stations = {}
                    add_ev_charging_stations = home_ev_charging_stations_network_updater(
                        penetration_percent=ev_penetration,
                        ev_p_w=ev_p_w,
                        ev_q_var=ev_q_var,
                        connection_point_ids=set(),
                        exclude_connections=True,
                        added_ev_stations=added_ev_stations
                    )

                    print(f"Added home EV Charging stations until {ev_penetration}% penetration ...")
                    pp_net = await add_ev_charging_stations(
                        pp.pandapowerNet(pp_initial_net),
                        result.mappings
                    )
                    print(f"Finished adding home EV charging stations")

                    # Run Load Flow
                    print(f"Running load flow ...")
                    pp.runpp(pp_net, numba=False, run_control=True)
                    print(f"Ran load flow")

                    # Upload Study
                    print(f"Uploading study ...")
                    upload_ev_charging_study(
                        eas_client,
                        pp_net,
                        f"Hosting Capacity Study ({ev_penetration}% EV charging penetration)",
                        f"Hosting capacity study with {ev_penetration}% of home EV charging station penetration."
                        f" Each EV charging station adds {ev_p_w / 1000}kW of real power"
                        f" and {ev_q_var / 1000}kVAR reactive power as load.",
                        ["ev_charging", feeder_mrid],
                        json.load(open("../src\\utils\\style.json", "r")),
                        result.mappings,
                        added_ev_stations
                    )
                    print(f"Uploaded study")
            else:
                logger.error(f"Failed to pass pandapower diagnostic check:\n{diagnostic}")
        else:
            logger.error(f"Failed to create pandapower network for feeder {feeder_mrid}")


async def get_load_providers(network: NetworkService, study_args: Dict) -> Tuple[
    Callable[[ConductingEquipment], Tuple[float, float]],
    Callable[[ConductingEquipment], Tuple[float, float]]
]:
    cust_load = {}
    pv_load = {}
    for pt in network.objects(PowerTransformer):
        # EnergyConsumers
        customer_count = await _num_of_consumers(pt)
        p_w = study_args["initial"]["load"]["real_w"]
        q_var = study_args["initial"]["load"]["reactive_var"]
        cust_load[pt.mrid] = (p_w * customer_count, q_var * customer_count)

        # PowerElectronicConnections
        pec_count = len(list(filter(lambda x: isinstance(x, PowerElectronicsConnection), await get_downstream_eq(pt))))
        p_w = study_args["initial"]["pv_load"]["real_w"]
        q_var = study_args["initial"]["pv_load"]["reactive_var"]
        pv_load[pt.mrid] = (p_w * pec_count, q_var * pec_count)

    def transformer_customer_load_provider(ce: ConductingEquipment) -> Tuple[float, float]:
        return cust_load.get(ce.mrid, (0.0, 0.0))

    def transformer_pv_load_provider(ce: ConductingEquipment) -> Tuple[float, float]:
        return pv_load.get(ce.mrid, (0.0, 0.0))

    return transformer_customer_load_provider, transformer_pv_load_provider


async def _get_feeder_network(channel, feeder_mrid) -> NetworkService:
    client = NetworkConsumerClient(channel)
    (await client.get_equipment_container(mrid=feeder_mrid, expected_class=Feeder)).throw_on_error()
    network = client.service
    feeder = network.get(feeder_mrid)
    _add_energy_source_at_feeder_head(network, feeder)
    _add_default_impedance_and_wire_info_to_lines(network)
    return client.service


def _add_energy_source_at_feeder_head(network: NetworkService, feeder: Feeder) -> NetworkService:
    es = EnergySource(mrid=f"{feeder.mrid}_es")
    es.base_voltage = feeder.normal_head_terminal.conducting_equipment.base_voltage
    es.location = feeder.normal_head_terminal.conducting_equipment.location
    es_t = Terminal(mrid=f"{es.mrid}-t", conducting_equipment=es, phases=PhaseCode.ABC, sequence_number=1)
    es.add_terminal(es_t)
    network.add(es)
    network.add(es_t)
    network.connect_by_mrid(es_t, feeder.normal_head_terminal.connectivity_node_id)

    return network


def _add_default_impedance_and_wire_info_to_lines(network: NetworkService) -> NetworkService:
    # PerLengthSequenceImpedance
    default_plsi = PerLengthSequenceImpedance()
    default_plsi.mrid = "default-plsi"
    default_plsi.r = 0.0004839
    default_plsi.r0 = 0.0006339
    default_plsi.x = 0.0003771
    default_plsi.x0 = 0.0015921
    network.add(default_plsi)

    # WireInfo
    default_wi = OverheadWireInfo()
    default_wi.rated_current = 1000
    network.add(default_wi)

    for acls in network.objects(AcLineSegment):
        if acls.per_length_sequence_impedance is None and acls.length != 0:
            acls.per_length_sequence_impedance = default_plsi
        if acls.wire_info is None and acls.length != 0:
            acls.asset_info = default_wi

    return network


def _remove_lv(network: NetworkService) -> NetworkService:
    io_to_remove = []
    for ce in network.objects(ConductingEquipment):
        if isinstance(ce, PowerTransformer):
            for end in ce.ends:
                if end.rated_u < 1000:
                    if end.terminal is not None:
                        ce.remove_terminal(end.terminal)
                        end.terminal = None
            continue

        if ce.base_voltage is None or ce.base_voltage.nominal_voltage < 1000:
            for t in ce.terminals:
                if t.connectivity_node is not None:
                    network.disconnect(t)
                io_to_remove.append(t)
            ce.clear_terminals()
            io_to_remove.append(ce)

    for io in io_to_remove:
        network.remove(io)

    return network


def home_ev_charging_stations_network_updater(
        penetration_percent: float,
        ev_p_w: float,
        ev_q_var: float,
        connection_point_ids: Set[str],
        exclude_connections: bool,
        added_ev_stations: Dict[str, int]
) -> Callable[[pp.pandapowerNet, BusBranchNetworkCreationMappings], pp.pandapowerNet]:
    async def ev_stations_adder(net: pp.pandapowerNet, mappings: BusBranchNetworkCreationMappings) -> pp.pandapowerNet:
        nonlocal connection_point_ids
        nonlocal exclude_connections
        nonlocal added_ev_stations

        pt_to_info = await _get_power_transformer_to_bus(mappings)
        allowed_dist_pt_info = _get_dist_pt_info(pt_to_info, connection_point_ids, exclude_connections)
        total_customer_count = reduce(lambda a, b: a + b.customer_count, allowed_dist_pt_info, 0)

        count = 0
        additional_ev_stations = ceil(total_customer_count * (penetration_percent / 100))

        while count < additional_ev_stations:
            pt_info = choice(allowed_dist_pt_info)

            if pt_info.customer_count == 0:
                continue

            pp.create_load(
                net,
                pt_info.bus_idx,
                ev_p_w / 1000000,
                ev_q_var / 1000000
            )
            pt_info.customer_count -= 1
            count += 1
            added_ev_stations[pt_info.name] = added_ev_stations.get(pt_info.name, 0) + 1

        return net

    return ev_stations_adder


async def _get_power_transformer_to_bus(mappings: BusBranchNetworkCreationMappings) -> Dict[str, DistTransformerInfo]:
    pt_to_busses = {}
    pts = {next(iter(pts)) for pts in mappings.to_nbn.power_transformers.values()}
    for pt in pts:
        for e in mappings.to_bbn.objects[pt.mrid]:
            if e.type == "bus":
                customer_count = await _num_of_consumers(pt)
                pt_to_busses[pt.mrid] = DistTransformerInfo(int(e.index), customer_count, pt.name)

    return pt_to_busses


# noinspection PyDefaultArgument
async def _num_of_consumers(pt: PowerTransformer, pt_to_num_consumers={}):
    if pt_to_num_consumers.get(pt.mrid) is not None:
        return pt_to_num_consumers.get(pt.mrid)

    num_of_c = len(list(filter(lambda x: isinstance(x, EnergyConsumer), await get_downstream_eq(pt))))
    pt_to_num_consumers[pt.mrid] = num_of_c
    return pt_to_num_consumers.get(pt.mrid, 0)


def _get_dist_pt_info(
        pt_to_info: Dict[str, DistTransformerInfo],
        connection_point_ids: Set[str],
        exclude_connections: bool
) -> List[DistTransformerInfo]:
    if exclude_connections:
        connections_busses = {pt_to_info[cpi].bus_idx for cpi in connection_point_ids}
        return list({info for info in pt_to_info.values() if info.bus_idx not in connections_busses})
    else:
        return list({pt_to_info[cpi] for cpi in connection_point_ids})


def _add_regulator_controllers(
        net: pp.pandapowerNet,
) -> pp.pandapowerNet:
    df = net.trafo[net.trafo["vn_hv_kv"] == net.trafo["vn_lv_kv"]]
    for i in df.index:
        # TapChanger values
        net.trafo.at[i, 'tap_max'] = 16
        net.trafo.at[i, 'tap_neutral'] = 0
        net.trafo.at[i, 'tap_min'] = -16
        net.trafo.at[i, 'tap_step_percent'] = 0.625
        net.trafo.at[i, 'tap_step_degree'] = 0
        net.trafo.at[i, 'tap_side'] = "lv"
        net.trafo.at[i, 'tap_pos'] = 0

        # Impedance values
        net.trafo.at[i, 'vk_percent'] = 0.5
        net.trafo.at[i, 'vkr_percent'] = 0.13
        net.trafo.at[i, 'pfe_kw'] = 0
        net.trafo.at[i, 'i0_percent'] = 0

        # Controller
        control.DiscreteTapControl(
            net=net,
            tid=i,
            vm_upper_pu=1.01,
            vm_lower_pu=.99
        )

    return net
