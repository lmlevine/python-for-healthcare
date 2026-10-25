import numpy as np
import pandas as pd
import simpy
from scipy import stats

# Kestrel Valley Health birth center (fictional). The structure follows Mark Isken's teaching
# model of an obstetrics unit: triage (OBS) -> labor, delivery and recovery (LDR) -> postpartum (PP).
# Times are in hours.
BASELINE = {
    "arrivals_per_day": 9.6,   # about 3,500 births a year
    "obs_beds": 4,             # triage beds
    "ldr_rooms": 7,
    "pp_beds": 26,
    "obs_hours": 3,            # average stay in each unit
    "ldr_hours": 12,
    "pp_hours": 48,
}
WARMUP_DAYS = 30               # the unit starts empty, so ignore the first month
RUN_DAYS = 365
MAX_TRIAGE_WAIT_H = 12         # past this average wait, a real unit would divert patients


def check_capacity(params):
    """Refuse to run a unit whose average demand meets or exceeds its beds: its queue never settles."""
    per_hour = params["arrivals_per_day"] / 24
    for unit, beds in [("obs", "obs_beds"), ("ldr", "ldr_rooms"), ("pp", "pp_beds")]:
        demand = per_hour * params[f"{unit}_hours"]          # beds busy on average
        if demand >= params[beds]:
            raise ValueError(f"Refusing to run: {unit.upper()} needs {demand:.1f} beds on average but has "
                             f"{params[beds]}. The queue would grow without limit.")


def simulate_year(params, seed):
    """Simulate one year of the birth center and return one row of results."""
    check_capacity(params)
    rng = np.random.default_rng(seed)
    env = simpy.Environment()
    obs = simpy.Resource(env, capacity=params["obs_beds"])
    ldr = simpy.Resource(env, capacity=params["ldr_rooms"])
    pp = simpy.Resource(env, capacity=params["pp_beds"])
    patients = []

    def patient(stays):
        arrived = env.now
        obs_bed = obs.request()
        yield obs_bed                          # wait for a triage bed
        wait_obs = env.now - arrived
        yield env.timeout(stays["obs"])

        ready = env.now
        ldr_room = ldr.request()
        yield ldr_room                         # wait for an LDR room, still holding the triage bed
        obs.release(obs_bed)
        wait_ldr = env.now - ready
        yield env.timeout(stays["ldr"])

        ready = env.now
        pp_bed = pp.request()
        yield pp_bed                           # blocked: wait for a PP bed, still holding the LDR room
        ldr.release(ldr_room)
        blocked = env.now - ready
        yield env.timeout(stays["pp"])
        pp.release(pp_bed)

        if arrived >= WARMUP_DAYS * 24:        # count only patients who arrive after the warm-up
            patients.append((wait_obs, wait_ldr, blocked))

    def arrivals():
        while True:
            yield env.timeout(rng.exponential(24 / params["arrivals_per_day"]))
            if env.now > (WARMUP_DAYS + RUN_DAYS) * 24:
                return                         # stop admitting, and let everyone already here finish
            # Each patient's stays are drawn when she arrives, so two scenarios run with
            # the same seed see exactly the same patients.
            stays = {unit: rng.exponential(1.0) * params[f"{unit}_hours"] for unit in ("obs", "ldr", "pp")}
            env.process(patient(stays))

    env.process(arrivals())
    env.run()                                  # until the last patient goes home

    wait_obs, wait_ldr, blocked = np.array(patients).T
    return {
        "births counted": len(patients),
        "waited for a triage bed (%)": 100 * (wait_obs > 0).mean(),
        "mean wait for a triage bed, all patients (h)": wait_obs.mean(),
        "waited for an LDR room (%)": 100 * (wait_ldr > 0).mean(),
        "mean wait for an LDR room, all patients (h)": wait_ldr.mean(),
        "blocked in LDR, waiting for PP (%)": 100 * (blocked > 0).mean(),
    }


def run_many(params, n=30, first_seed=1):
    """Run n replications (one per seed) and return one row per replication."""
    return pd.DataFrame([simulate_year(params, seed) for seed in range(first_seed, first_seed + n)])


def summarize(results, min_reps=20):
    """Mean and 95% interval for each result. Refuses to report numbers that don't mean anything."""
    n = len(results)
    if n < min_reps:
        raise ValueError(f"Refusing to summarize {n} replication(s): run at least {min_reps}. "
                         "One run is an anecdote.")
    triage_wait = results["mean wait for a triage bed, all patients (h)"].mean()
    if triage_wait > MAX_TRIAGE_WAIT_H:
        raise ValueError(f"Refusing to summarize: patients waited {triage_wait:.0f} hours for a triage bed on "
                         "average. A real unit would divert patients long before that, and this model can't.")
    t = stats.t.ppf(0.975, n - 1)
    mean = results.mean()
    half = t * results.std() / np.sqrt(n)
    return pd.DataFrame({"mean": mean.round(1),
                         "95% interval": [f"{m - h:.1f} to {m + h:.1f}" for m, h in zip(mean, half)]})
