import collections
import collections.abc
collections.Iterable = collections.abc.Iterable
from pathlib import Path
from typing import List
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from hedra.plugins.types.common import Event
from hedra.plugins.types.reporter import (
    ReporterConfig,
    ReporterPlugin,
    Metrics,
    connect,
    close,
    process_events,
    process_shared,
    process_metrics,
    process_custom,
    process_errors
)


class XMLReporterConfig(ReporterConfig):
    events_filepath: str = None
    metrics_filepath: str = None


class XMLReporter(ReporterPlugin[XMLReporterConfig]):
    config=XMLReporterConfig
    
    def __init__(self, config: XMLReporterConfig) -> None:
        super().__init__(config)

    @connect()
    async def connect_xml_reporter(self):
        pass
    
    @process_events()
    async def save_events_as_xml(self, events: List[Event]):
        events_xml = dicttoxml([
            event.to_dict() for event in events
        ], custom_root='events')

        events_xml = parseString(events_xml)

        with open(self.config.events_filepath, 'a') as events_file:
            await self.loop.run_in_executor(
                self.executor,
                events_file.write,
                events_xml.toprettyxml()
            )

    @process_shared()
    async def save_shared_as_xml(self, metrics: List[Metrics]):

        common_metrics_xml = dicttoxml([
            {
                'name': metric_set.name,
                'stage': metric_set.stage,
                'group': 'common',
                **metric_set.common_stats
            } for metric_set in metrics
        ], custom_root='common_metrics')

        common_metrics_xml = parseString(common_metrics_xml)

        base_filepath = Path(self.config.metrics_filepath).parent
        with open(f'{base_filepath}/stage_metrics.xml', 'w') as shared_metrics_file:
            await self.loop.run_in_executor(
                self.executor,
                shared_metrics_file.write,
                common_metrics_xml.toprettyxml()
            )

    @process_metrics()
    async def save_metrics_as_xml(self, metrics: List[Metrics]):

        metrics_data = []
        for metrics_set in metrics:
            for group_name, group in metrics_set.groups.items():
                metrics_data.append({
                    **group.record,
                    'group': group_name
                })


        metrics_xml = dicttoxml(metrics_data, custom_root='metrics')
        metrics_xml = parseString(metrics_xml)

        with open(self.config.metrics_filepath, 'a') as metrics_file:
            await self.loop.run_in_executor(
                self.executor,
                metrics_file.write,
                metrics_xml.toprettyxml()
            )

    @process_custom()
    async def save_custom_metrics_as_xml(self, metrics: List[Metrics]):

        metrics_data = []
        for metrics_set in metrics:
            for custom_group_name, custom_group in metrics_set.custom_metrics.items():
                metrics_data.append({
                    **custom_group,
                    'group': custom_group_name
                })

        custom_metrics_xml = dicttoxml(metrics_data, custom_root='custom_metrics')
        custom_metrics_xml = parseString(custom_metrics_xml)

        with open(self.config.metrics_filepath, 'a') as custom_metrics_file:
            await self.loop.run_in_executor(
                self.executor,
                custom_metrics_file.write,
                custom_metrics_xml.toprettyxml()
            )

    @process_errors()
    async def save_errors_as_xml(self, metrics: List[Metrics]):

        errors = []
        for metrics_set in metrics:
            for error in metrics_set.errors:
                errors.append({
                    'name': metrics_set.name,
                    'stage': metrics_set.stage,
                    'error_message': error.get('message'),
                    'error_count': error.get('count')
                })

        errors_xml = dicttoxml(errors, custom_root='errors')
        errors_xml = parseString(errors_xml)

        with open(self.config.metrics_filepath, 'a') as errors_file:
            await self.loop.run_in_executor(
                self.executor,
                errors_file.write,
                errors_xml.toprettyxml()
            )

    @close()
    async def close_xml_reporter(self):
        pass