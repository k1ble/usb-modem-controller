import subprocess
import shutil
import json
import os

from logger import  logger

def_config = {"ADB" : None, "default_mode" : "rndis"}
config_name = "config.json"

def load_config():
    if not os.path.exists(config_name):
        save_config(def_config)
    try:
        with open(config_name, "r") as f:
            logger.info(f"loading {config_name}... ")
            return json.load(f)
    except (json.JSONDecodeError):
        logger.error(f"{config_name} not founded, creating file...")
        save_config(def_config)
        return json.load(f)
        
def save_config(val):
    logger.info("config changed...")
    with open(config_name, "w") as f:
        return json.dump(val, f)
    
config_dict = dict(load_config())

ADB = config_dict.get("ADB")
if not ADB:    
    try:
        ADB = shutil.which("adb")
        def_config["ADB"] = ADB
        save_config(def_config)
    except:
        logger.critical("Can't find ADB...")
        raise RuntimeError("You don't have adb. please, install adb and add it to PATH.")
    
target_mode = config_dict.get("default_mode")
if not target_mode:
    target_mode = "rndis"
    
def adbRun(*command):
    comlist =  [ADB] + list(command)        
        
    process = subprocess.run (
    comlist,
    text = True,
    capture_output= True,
    )
    return {
            "stdout": process.stdout,
            "Rcode": process.returncode, 
            "last_command": list(command),
            "stderr": process.stderr,
            }

def run_RND():
    global target_mode
    target_mode = "rndis"
    
    logger.info("Running rndis...")
    return adbRun("shell", "svc", "usb", "setFunctions", "rndis")

def run_MTP():
    global target_mode
    target_mode = "mtp"
    
    logger.info("Running MTP...")
    return adbRun("shell", "svc", "usb", "setFunctions", "mtp")

def run_USB_reset():
    logger.info("Reseting USB...")
    return adbRun("shell", "svc", "usb", "resetUsbGadget")

def get_target_mode():
    return target_mode
        
def get_full_status():
    adb_out = adbRun("devices")
    legacy_mode = adbRun("shell", "svc", "usb", "getFunctions")
    
    out = adb_out.get("stdout") 
    code = adb_out.get("Rcode")
    stderr = adb_out.get("stderr")
    st_mode = legacy_mode.get("stdout") or legacy_mode.get("stderr").strip()
    
    if code == 0:
        for device in out.splitlines():
            if "unauthorized" in device:
                logger.warning("Device unauthorized")
                return {
                    "connect": False,
                    "mode": "unauthorized",
                    "device_id": device,
                    "stderr":stderr,
                    "stdout":out,
                }
                
            if '\tdevice' in device:
                return {
                        "connect": True,
                        "mode": st_mode,
                        "device_id": device,
                        "stderr":stderr,
                        "stdout":out,
                        }
    return {
            "connect": False,
            "mode": None,
            "device_id": None,
            "stderr":stderr,
            "stdout": None,
            }         
                
status = get_full_status()