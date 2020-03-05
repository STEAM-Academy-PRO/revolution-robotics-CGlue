import json
import os
import argparse
import sys

from .component import Component
from .cglue import CGlue
from .plugins.AsyncServerCalls import async_server_calls
from .plugins.BuiltinDataTypes import builtin_data_types
from .plugins.Locks import locks
from .plugins.ProjectConfigCompactor import project_config_compactor
from .plugins.RuntimeEvents import runtime_events
from .plugins.UserCodePlugin import user_code_plugin
from .utils.filesystem import FileTransaction


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', help='Name of project config json file', default="./project.json")
    parser.add_argument('--cleanup', help='Delete backup files after code generation', action='store_true')
    parser.add_argument('--cglue-output', help='Name of the generated files', default='./generated/cglue')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--new-project', help='Create new CGlue project')
    group.add_argument('--new-component', help='Create new software component')
    group.add_argument('--update-component', help='Update software component')
    group.add_argument('--update-all-components', help='Update all software components', action='store_true')
    group.add_argument('--generate', help='Generate glue code', action="store_true")

    args = parser.parse_args()

    ft = FileTransaction(os.path.realpath(os.path.dirname(args.project)))

    if args.new_project:
        project_name = args.new_project
        project = {
            "settings": {
                "name": project_name,
                "components_folder": "src/SwComponents",
                "required_plugins": [
                    "ProjectConfigCompactor",
                    "BuiltinDataTypes",
                    "RuntimeEvents"
                ]
            },
            "sources": [
                "src/main.c",
                "src/generated/cglue.c"
            ],
            "includes": [
                "src",
                "src/generated"
            ],
            "components": [],
            "types": {
                "uint8_t": {
                    "pass_semantic": "value",
                    "defined_in": "<stdint.h>",
                    "default_value": "0u"
                },
                "uint8_t*": {
                    "pass_semantic": "value",
                    "defined_in": "<stdint.h>",
                    "default_value": "NULL"
                },
                "const uint8_t*": {
                    "pass_semantic": "value",
                    "defined_in": "<stdint.h>",
                    "default_value": "NULL"
                },
                "uint16_t": {
                    "pass_semantic": "value",
                    "defined_in": "<stdint.h>",
                    "default_value": "0u"
                },
                "uint32_t": {
                    "pass_semantic": "value",
                    "defined_in": "<stdint.h>",
                    "default_value": "0u"
                },
                "int8_t": {
                    "pass_semantic": "value",
                    "defined_in": "<stdint.h>",
                    "default_value": "0"
                },
                "int16_t": {
                    "pass_semantic": "value",
                    "defined_in": "<stdint.h>",
                    "default_value": "0"
                },
                "int32_t": {
                    "pass_semantic": "value",
                    "defined_in": "<stdint.h>",
                    "default_value": "0"
                },
                "size_t": {
                    "pass_semantic": "value",
                    "defined_in": "<stdio.h>",
                    "default_value": "0u"
                },
                "bool": {
                    "pass_semantic": "value",
                    "defined_in": "<stdbool.h>",
                    "default_value": "false"
                },
                "float": {
                    "pass_semantic": "value",
                    "defined_in": "<float.h>",
                    "default_value": "0.0f"
                },
                "ByteArray_t": {
                    "type": "struct",
                    "pass_semantic": "value",
                    "fields": {
                        "bytes": "uint8_t*",
                        "count": "size_t"
                    }
                },
                "ConstByteArray_t": {
                    "type": "struct",
                    "pass_semantic": "value",
                    "fields": {
                        "bytes": "const uint8_t*",
                        "count": "size_t"
                    }
                },
                "QueueStatus_t": {
                    "type": "enum",
                    "pass_semantic": "value",
                    "values": [
                        "QueueStatus_Empty",
                        "QueueStatus_Ok",
                        "QueueStatus_Overflow"
                    ],
                    "default_value": "QueueStatus_Empty"
                }
            },
            "runtime": {
                "runnables": {
                    "OnInit": []
                },
                "port_connections": []
            }
        }
        files = {
            args.project: json.dumps(project, indent=4)
        }
        ft.create_folder('src')
        ft.create_folder('src/generated')
        ft.create_folder('src/SwComponents')
    else:
        rt = CGlue(args.project)
        rt.add_plugin(project_config_compactor())
        rt.add_plugin(builtin_data_types())
        rt.add_plugin(runtime_events())
        rt.add_plugin(locks())
        rt.add_plugin(user_code_plugin())
        rt.add_plugin(async_server_calls())
        rt.load()

        if args.new_component:
            project_config = rt._project_config
            component_name = args.new_component
            if component_name in project_config['components']:
                print('Component already exists')
                sys.exit(1)

            component_config = {
                'name': component_name,
                'source_files': [component_name + '.c'],
            }

            rt.add_component(Component(component_name, component_config, rt.types))

            project_config['components'].append(component_name)
            project_config['components'] = sorted(project_config['components'])

            ft.create_folder(os.path.join(rt.settings['components_folder'], component_name))

            # add component to project json
            ft.update_file('project.json', rt.dump_project_config())

            files = rt.update_component(component_name)

        elif args.update_component:
            component_name = args.update_component
            files = rt.update_component(component_name)

        elif args.update_all_components:
            files = {}
            for component_name in rt._components:
                if component_name != 'Runtime':
                    files.update(rt.update_component(component_name))

        elif args.generate:
            files = rt.generate_runtime(args.cglue_output)

        else:
            parser.print_help()
            return

    for file_name, contents in files.items():
        ft.update_file(file_name, contents)
    ft.apply(delete_backups=args.cleanup)


if __name__ == '__main__':
    cli()
