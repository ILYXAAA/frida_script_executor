import zipfile
import os
import pathlib
from jawa.cf import ClassFile
from Colors import Colors
import random

def decompile_apk(apk_file, apk_file_name):
    os.system(f'dex-tools-v2.4\d2j-dex2jar "{apk_file}"')
    if os.path.exists(apk_file.replace(".apk", "") + "-dex2jar.jar"):
        print(f"File {apk_file_name} was decompiled")
        return True
    else:
        print(f"Something went wrong while decompiling")
        return False

def unzip_jar_file(apk_file, apk_file_name):
    jar_file = zipfile.ZipFile(f"{apk_file_name.replace('.apk', '')}-dex2jar.jar", "r")
    output_directory = f"{apk_file_name}_output/"

    for item in jar_file.namelist():
        jar_file.extract(item, output_directory)

    jar_file.close()
    print(f"File {apk_file_name.replace('.apk', '')}-dex2jar.jar was extracted")

def extract_methods(class_file):
    methods = []
    for method in class_file.methods:
        methods.append(method.name.value)
    return methods

def make_trace_methods_script(apk_file):
    apk_file_name = apk_file.split("/")[-1]
    #Декомпиляция apk файла в jar файл
    result = decompile_apk(apk_file, apk_file_name)
    #input("Нажмите чтобы продолжить..")
    #Распаковка jar файла в output
    if not result:
        return False
    unzip_jar_file(apk_file, apk_file_name)
    
    output = pathlib.Path(f"{apk_file_name}_output/")
    output.rglob("*") 
    classes_names = []
    for file in list(output.rglob("*")):
        if "\\android\\" not in str(file) and ".class" in str(file):
            classes_names.append(str(file).replace("\\", "/"))

    decompiled_classes_and_methods = {}
    for class_file_path in classes_names:
        with open(class_file_path, 'rb') as file:
            class_file = ClassFile(file)
            methods = extract_methods(class_file)
            if methods:
                cleaned_methods = []
                for method in methods:
                    if "<" not in method or ">" not in method:
                        cleaned_methods.append(method)
                if cleaned_methods:
                    class_name = class_file_path.replace(f"{apk_file_name}_output/", "").replace("/", ".").replace(".class", "")
                    decompiled_classes_and_methods[class_name] = cleaned_methods

    #print(decompiled_classes_and_methods)
    # Define your configurations
    # configurations = [
    #     {"className": f"jakhar.aseem.diva.AccessControl1Activity", "color": {Colors.BLUE}, "methods": ["onCreate", "viewAPICredentials"]},
    #     {"className": f"jakhar.aseem.diva.AccessControl2Activity", "color": {Colors.RED}, "methods": ["onCreate", "viewAPICredentials"]},
    #     # Add more configurations as needed
    # ]
    configurations = []
    for java_class in decompiled_classes_and_methods:
        configurations.append({"className": f"{java_class}", "color": random.choice(Colors.ALL_COLORS_LIST), "methods": decompiled_classes_and_methods[java_class]})



    # Create the Java code template
    java_code_template = f"""
    Java.perform(function () {{
        var classesAndMethods = {configurations};

        for (let i = 0; i < classesAndMethods.length; i++) {{
            let classInfo = classesAndMethods[i];
            let targetClass = Java.use(classInfo.className);

            for (let j = 0; j < classInfo.methods.length; j++) {{
                let methodName = classInfo.methods[j];

                targetClass[methodName].implementation = function () {{
                    console.log("")
                    console.log("\033[1m" + "===" + "\x1b[0m")
                    console.log(classInfo.color + "Function called in " + classInfo.className + "\x1b[0m"); // Reset color

                    // Print information about the function, parameters, and return value
                    console.log(classInfo.color + "Function: "  + "\x1b[0m" + classInfo.className + "." + methodName);
                    console.log(classInfo.color + "Arguments: "  + "\x1b[0m" + JSON.stringify(arguments));

                    // Execute the original method
                    let result = this[methodName].apply(this, arguments);

                    // Print information about the return value
                    console.log(classInfo.color + "Return Value: "  + "\x1b[0m" + JSON.stringify(result));

                    // Add a delay of 1 second (adjust as needed)
                    setTimeout(function () {{}}, 1500);

                    return result;
                }};
            }}
        }}
    }});
    """

    # Write the Java code to a .js file
    with open(f"{apk_file_name}_trace_methods.js", "w") as file:
        file.write(java_code_template)

    print("Java code saved")
    return True



