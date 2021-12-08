from typing import List

from zepben.evolve import ConductingEquipment, Traversal, SinglePhaseKind, PhaseDirection, LifoQueue


async def get_downstream_eq(ce: ConductingEquipment) -> List[ConductingEquipment]:
    eqs: List[ConductingEquipment] = []
    trace = Traversal(
        start_item=ce,
        queue_next=queue_downstream_equipment,
        process_queue=LifoQueue(),
        step_actions=[collect_eq_in(eqs)]
    )
    await trace.trace()
    return eqs


def queue_upstream_equipment(ce: ConductingEquipment, exclude=None):
    downstream_equipment = []
    for t in ce.terminals:

        for ot in t.connectivity_node.terminals:
            if ot.traced_phases.direction_normal(SinglePhaseKind.A).has(PhaseDirection.OUT):
                is_downstream = True
            elif ot.traced_phases.direction_normal(SinglePhaseKind.B).has(PhaseDirection.OUT):
                is_downstream = True
            elif ot.traced_phases.direction_normal(SinglePhaseKind.C).has(PhaseDirection.OUT):
                is_downstream = True
            else:
                is_downstream = False
            if ot != t and is_downstream:
                downstream_equipment.append(ot.conducting_equipment)

    return downstream_equipment


def queue_downstream_equipment(ce: ConductingEquipment, exclude=None):
    downstream_equipment = []
    for t in ce.terminals:

        for ot in t.connectivity_node.terminals:
            if ot.traced_phases.direction_normal(SinglePhaseKind.A).has(PhaseDirection.IN):
                is_downstream = True
            elif ot.traced_phases.direction_normal(SinglePhaseKind.B).has(PhaseDirection.IN):
                is_downstream = True
            elif ot.traced_phases.direction_normal(SinglePhaseKind.C).has(PhaseDirection.IN):
                is_downstream = True
            else:
                is_downstream = False
            if ot != t and is_downstream:
                downstream_equipment.append(ot.conducting_equipment)

    return downstream_equipment


def collect_eq_in(collection: List[ConductingEquipment]):
    async def add_eq(ce, _):
        collection.append(ce)

    return add_eq
