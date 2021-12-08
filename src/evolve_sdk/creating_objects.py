#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import PowerTransformer, EnergyConsumer, PhotoVoltaicUnit, BatteryUnit, BaseVoltage, \
    PerLengthSequenceImpedance, OverheadWireInfo, PowerTransformerInfo, AcLineSegment


def creating_objects():
    print('Creating objects...')
    # Create Base Voltages
    bv_hv: BaseVoltage = BaseVoltage(mrid="20kV", nominal_voltage=20000, name="20kV")
    bv_lv: BaseVoltage = BaseVoltage(mrid="415V", nominal_voltage=3000, name="415V")

    print(bv_lv)
    print(f'Nominal voltage for {bv_lv}: {bv_hv.nominal_voltage} Volts')

    # PerLengthSequenceImpedance
    plsi = PerLengthSequenceImpedance(
        mrid="psli",
        r=0.642 / 1000,
        x=0.083 / 1000
    )

    print(plsi)
    print(f'r, x  for {plsi}: {plsi.r} Ohms, {plsi.x} Ohms')

    # WireInfo
    wire_info = OverheadWireInfo(
        mrid="wire_info",
        rated_current=0.142 * 1000
    )

    print(wire_info)
    print(f'Rated current for {wire_info}: {wire_info.rated_current} A')

    # Line
    line = AcLineSegment(mrid="line", name="Line", length=100.0, per_length_sequence_impedance=plsi)
    line.asset_info = wire_info
    line.base_voltage = bv_lv

    print(line)
    print(f'PerLengthSequence resistance of line {line.mrid}: {line.per_length_sequence_impedance.r}')
    print(f'PerLengthSequence resistance of line {line.mrid}: {line.per_length_sequence_impedance.r}')

    # PowerTransformerInfo
    pt_info = PowerTransformerInfo(
        mrid="pt_info"
    )

    # Create a Power Transformer
    power_transformer = PowerTransformer(mrid="pt1")
    print(power_transformer)

    # Create EnergyConsumer
    energy_consumer = EnergyConsumer(mrid="ec1")
    print(energy_consumer)

    # Create Photovoltaic Unit
    pv_unit = PhotoVoltaicUnit(mrid="pv1")
    print(pv_unit)

    # Create Battery
    battery = BatteryUnit(mrid="b1")
    print(battery)


if __name__ == '__main__':
    creating_objects()
