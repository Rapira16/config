import os
import zipfile
import xml.etree.ElementTree as ET
import argparse

def extract_dependencies(nupkg_path):
    dependencies = {}
    with zipfile.ZipFile(nupkg_path, 'r') as z:
        for filename in z.namelist():
            if filename.endswith('.nuspec'):
                with z.open(filename) as file:
                    tree = ET.parse(file)
                    root = tree.getroot()
                    ns = {'n': root.tag.split('}')[0].strip('{')}
                    for dep_group in root.findall('.//n:dependencies', ns):
                        for dep in dep_group.findall('.//n:dependency', ns):
                            package = dep.attrib['id']
                            version = dep.attrib['version']
                            dependencies[package] = version
    return dependencies

def generate_plantuml(dependencies):
    plantuml_code = "@startuml\n"
    for dep, version in dependencies.items():
        plantuml_code += f"[{dep} {version}] --> [YourPackage]\n"
    plantuml_code += "@enduml"
    return plantuml_code

def main():
    parser = argparse.ArgumentParser(description="Dependency Graph Visualizer for .NET packages")
    parser.add_argument("nupkg_path", help="Path to the .NET package file")
    parser.add_argument("output_path", help="Path to output the result code")
    args = parser.parse_args()

    dependencies = extract_dependencies(args.nupkg_path)
    plantuml_code = generate_plantuml(dependencies)

    with open(args.output_path, 'w') as f:
        f.write(plantuml_code)

    print(f"PlantUML code has been written to {args.output_path}")

if __name__ == "__main__":
    main()
