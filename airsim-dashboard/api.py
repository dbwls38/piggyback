from fastapi import APIRouter
from core.simulation_core import SimulationCore

router = APIRouter()

# dummy placeholders
airsim = None
scenario_engine = None
hara_engine = None

core = SimulationCore(airsim, scenario_engine, hara_engine)

@router.post("/scenario")
def run(data: dict):
    return core.run_scenario(data["type"])

@router.post("/start")
def start():
    core.start()
    return {"status": "started"}

@router.post("/stop")
def stop():
    core.stop()
    return {"status": "stopped"}

@router.get("/state")
def state():
    return core.get_state()