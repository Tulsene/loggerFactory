# Logger Factory Framework
## About
This framework aim to provide an easy to use configuration for advanced logging configuration that work with multiple type of applications:
- simple application with one process and one thread,
- multithreaded applications,
- multiprocesses application where the logger is in the main process but on a separate thread,
- multiprocess application with a dedicated process for logging.

Example from the official documentation (with little or no modifications) are in `officialDocExamples` repository or can be found here `https://docs.python.org/3/howto/logging-cookbook.html`

## How it work
### Configuration
A logging configuration template is in `config`. You can add some custom configuration when initializing with `set_...` function from `utils.loggerFactory.py`.

### Usage
Then call the `get_..` function that fits to your needs. See `examples.py` to see how it should be used.

## Possible TODO
- Add the missing https://docs.python.org/3/library/logging.html#logrecord-attributes on regex pattern
- Add the possibility to create filters
- Sends logs directly to locki
- Add the posibility to change logging config during application runtime