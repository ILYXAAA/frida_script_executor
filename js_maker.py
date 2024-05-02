from Colors import Colors
import random

def make_js_script(decompiled_classes_and_methods):
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
                    setTimeout(function () {{}}, 1000);

                    return result;
                }};
            }}
        }}
    }});
    """

    # Write the Java code to a .js file
    with open("test.js", "w") as file:
        file.write(java_code_template)

    print("Java code saved to test.js")