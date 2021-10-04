from dataclasses import dataclass, field

from geojson import FeatureCollection
from zepben.eas import EasClient
from zepben.eas.client.study import Study

from utils.style_creator import BasicStyle


@dataclass
class StudyCreator:
    name: str
    tags: [str]
    styles: [BasicStyle]
    description: str = field(default='')
    results: [Study.Result] = field(init=False)

    def __post_init__(self):
        self.results = []
        self.study = Study(
            name=f"{self.name}",
            description=self.description,
            tags=self.tags,
            results=self.results,
            styles=self.styles
        )

    def add_result(self, name: str, styles: [str], feature_collection=None):
        if feature_collection is None:
            feature_collection = FeatureCollection(features=[])
        result = Study.Result(name=name, geo_json_overlay=Study.Result.GeoJsonOverlay(
            data=feature_collection,
            styles=styles
        ))
        self.study.results.append(result)

    def add_section(self, result: Study.Result, columns: [{str: str}], data: [{str: str}]):
        # todo: Finish this method.
        # todo: add section with results in tabular form
        """
        :param data:
        :param result:
        :param columns: [{"key": "xxx", "name": "yyy"}]
        :return: None
        """
        result.Section(
            type="TABLE",
            name=self.name,
            description='Description',
            columns=columns,
            data=data
        )

    def upload(self, eas_client: EasClient):
        if self.results:
            eas_client.upload_study(
                Study(
                    name=f"{self.name}",
                    description=self.description,
                    tags=self.tags,
                    results=self.results,
                    styles=self.styles
                )
            )
            print("Study has been uploaded to server")
        else:
            print(f'Study "{self.name}" has not been uploaded to server. No results were added  to the study.')
