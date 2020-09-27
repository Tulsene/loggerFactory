import logging.handlers
from multiprocessing import Process, Queue, Event
import os
import time
import threading


import utils.helpers as helper
import utils.loggerFactory as logger_factory
from utils.loggerFactory import Logger

root_path = helper.set_root_path()


def remove_existing_log_files() -> None:
    for file in os.listdir(f'{root_path}logs/'):
        os.remove(f'{root_path}logs/{file}')


def super_logs(log: Logger) -> None:
    for i in range(100):
        log.error(f'yey {i}')
        log.ext_warning(f'yey2 {i}')

        try:
            1/0
        except Exception as e:
            log.ext_exception(f'{e} {i}')

    log.debug(None)


def test_set_simple_logger() -> None:
    logger_factory.set_simple_logger(root_path)
    log = logger_factory.get_simple_logger('spam')
    super_logs(log)
    log = logger_factory.get_simple_logger('spam.ham')
    super_logs(log)


def worker_thread(log: Logger) -> None:
    super_logs(log)


def test_multi_thread_logger() -> None:
    logger_factory.set_simple_logger(root_path)
    log = logger_factory.get_simple_logger('spam.ham.yey')
    threads = []
    for i in range(5):
        thread = threading.Thread(target=worker_thread,
                                  name=f'thread {i + 1}',
                                  args=(log,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def worker_process(processes_queue: Queue) -> None:
    log = logger_factory.get_logger_in_process(processes_queue, 'spam.ham')
    super_logs(log)


def test_set_logger_in_separate_thread() -> None:
    processes_queue, logs_listener = \
        logger_factory.set_process_logger_in_separate_thread(root_path)
    workers = []
    for i in range(5):
        wp = Process(target=worker_process,
                     name=f'worker {(i + 1)}',
                     args=(processes_queue,))
        workers.append(wp)
        wp.start()

    for wp in workers:
        wp.join()

    q.put(None)
    logs_listener.join()


def worker_with_logging_seperate_worker(processes_queue: Queue) -> None:
    log = logger_factory.get_process_logging_config(processes_queue, 'spam')
    super_logs(log)


def test_with_logging_as_seperate_worker() -> None:
    processes_queue, stop_event, listener_process = \
        logger_factory.set_logger_in_separate_process(root_path)
    workers = []
    for i in range(5):
        wp = Process(target=worker_process,
                     name=f'worker {i + 1}',
                     args=(processes_queue,))
        workers.append(wp)
        wp.start()

    log = logger_factory.get_process_logging_config(processes_queue, 'spam')
    super_logs(log)

    for wp in workers:
        wp.join()

    stop_event.set()
    listener_process.join()


if __name__ == '__main__':
    remove_existing_log_files()
    # test_set_simple_logger()
    # test_multi_thread_logger()
    # test_set_logger_in_separate_thread()
    test_with_logging_as_seperate_worker()
