import os
import asyncio
import importlib


from stereotypes.generic.StereotypeScript import StereotypeScript


async def download_stereotype(stereotype_info) -> StereotypeScript:
    
    stereotype_base_module =  "stereotypes."
    
    def get_start_class(module):
            class_name = "Start"
            if hasattr(module, class_name):
                start = getattr(module, class_name)
                # Now you can use MyClass
                return start()
    
    try:
        module_name = stereotype_info["name"]
        # Try to import the module
        module = importlib.import_module(stereotype_base_module + module_name + ".Start")
        # get corresponding Start class
        return get_start_class(module)
    except ImportError:
        print(f"Module '{module_name}' is not installed. Upgrade stereotypes library...")
        try:
            
            process = await asyncio.create_subprocess_exec(
                #"pip", "install", "-e", "stereotypes"), #change when it will be osted on PyiP
                "pip", "install", "--upgrade", "stereotypes",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()
            if process.returncode == 0:
                print(f"Module '{module_name}' installed successfully.")
                module = importlib.import_module(stereotype_base_module + module_name + ".Start")
                return get_start_class(module)
                
            else:
                print(f"Error installing module '{module_name}':")
                print("STDOUT:", stdout.decode().strip())
                print("STDERR:", stderr.decode().strip())
        except Exception as e:
            print(f"Error installing module '{module_name}': {e}")
            
    
            
    

    