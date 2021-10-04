import pytest

from test.utils.style_creator import CircleStyle, LineStyle, CirclePaint, LinePaint, InterpolateColor
from geojson import Feature, FeatureCollection, Point, LineString

from zepben.eas import EasClient


@pytest.fixture
def eas_client(config):
    return EasClient(host=config.eas_server.host, port=config.eas_server.port,
                     client_id=config.auth0.client_id,
                     username=config.auth0.username,
                     password=config.auth0.password)


def test_upload_study(eas_client):
    feature1 = Feature(id='id1', geometry=Point((144.408936254, -37.6999353628)))
    feature2 = Feature(id='id2', geometry=Point((144.408936254, -37.99353628)))
    feature3 = Feature(id='id3', geometry=LineString([(144.408936254, -37.99353628), (144.408936254, -37.6999353628)]),
                       properties={"number": "100"})
    fc1 = FeatureCollection([feature1, feature2, feature3])
    fc2 = FeatureCollection([feature3])

    styles = [CircleStyle(style_id='circle').style,
              LineStyle(style_id='line').style,
              LineStyle(style_id='line_loading', paint=LinePaint(
                  line_color=InterpolateColor(to_number_name="number", limits=[0, 50, 100]).color()).paint).style,
              CircleStyle(style_id='circle2', paint=CirclePaint(color="red").paint).style]

    study = StudyCreator(name='Basic Study', tags=['basic_study'], styles=styles)
    study.add_result(name='2 x Circle &  1 x Line', feature_collection=fc1, styles=['circle', 'line'])
    study.add_result(name='1 x Line', feature_collection=fc2, styles=['line_loading'])
    study.upload(eas_client)

