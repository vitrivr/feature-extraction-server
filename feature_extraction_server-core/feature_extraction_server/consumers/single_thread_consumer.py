

def start(model, log_server):
    import multiprocessing as mp
    process = mp.Process(target=_run, args=(model, log_server))
    process.start()
    return process

def _run(model, log_server):
    log_server.configure_worker()
    model.load_model()
    for job in model.fetch_jobs():
        job.run()


