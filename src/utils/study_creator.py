from typing import List, Dict

import pandapower as pp
from geojson import FeatureCollection, Feature, Point, LineString
from zepben.eas import EasClient, Study
from zepben.evolve import BusBranchNetworkCreationMappings

__all__ = ["upload_load_flow_study"]


def upload_load_flow_study(
        client: EasClient,
        network: pp.pandapowerNet,
        name: str,
        description: str,
        tags: List[str],
        styles: List,
        mappings: BusBranchNetworkCreationMappings
) -> None:
    client.upload_study(
        Study(
            name=name,
            description=description,
            tags=tags,
            results=[
                *[
                    Study.Result(
                        name="Tx & Line Thermal Capacity",
                        geo_json_overlay=Study.Result.GeoJsonOverlay(
                            data=to_tx_line_utilisation_geojson(network, mappings),
                            styles=[s['id'] for s in styles]
                        )
                    ),
                    Study.Result(
                        name="Voltage Per-Unit",
                        geo_json_overlay=Study.Result.GeoJsonOverlay(
                            data=to_voltage_pu_geojson(network),
                            styles=[s['id'] for s in styles]
                        )
                    )
                ]
            ],
            styles=styles
        )
    )


def to_tx_line_utilisation_geojson(
        net: pp.pandapowerNet,
        mappings: BusBranchNetworkCreationMappings
) -> FeatureCollection:
    tx_geojson = []
    for index, tx_name in enumerate(net.trafo.name):
        pt = next(iter(mappings.to_nbn.power_transformers[f"trafo:{index}"]))
        loading_percent = net.res_trafo.iloc[index].loading_percent
        position = list(pt.location.points)[0]
        x = position.x_position
        y = position.y_position
        tx_geojson.append(
            Feature(
                tx_name,
                Point((x, y)),
                {
                    "name": tx_name,
                    "type": "tx",
                    "overload_percent": _format_decimal_value(loading_percent)
                }
            )
        )

    line_geojson = []
    for index, line_name in enumerate(net.line.name):
        coords = net.line_geodata.coords[index]
        loading_percent = net.res_line.iloc[index].loading_percent

        line_geojson.append(
            Feature(
                line_name,
                LineString(coords),
                {
                    "name": line_name,
                    "type": "line",
                    "overload_percent": _format_decimal_value(loading_percent)
                }))

    features = []
    for tx_f in tx_geojson:
        features.append(tx_f)

    for line_f in line_geojson:
        features.append(line_f)

    return FeatureCollection(features)


def to_voltage_pu_geojson(result: pp.pandapowerNet) -> FeatureCollection:
    bus_geodata: Dict = result.bus_geodata.to_dict()
    bus_results = result.res_bus.to_dict()

    bus_geojson = []
    for idx in range(len(bus_geodata["x"])):
        x = bus_geodata["x"][idx]
        y = bus_geodata["y"][idx]
        vm_pu = bus_results["vm_pu"][idx]
        bus_geojson.append(
            Feature(
                idx,
                Point((x, y)),
                {
                    "name": idx,
                    "type": "bus",
                    "vm_pu": _format_decimal_value_3d(vm_pu)
                }))

    features = []
    for bus_f in bus_geojson:
        features.append(bus_f)

    return FeatureCollection(features)


def _format_decimal_value(f: float):
    return float("{:.1f}".format(f))


def _format_decimal_value_3d(f: float):
    return float("{:.3f}".format(f))
