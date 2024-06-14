# Logger Setup for Sirji Framework

The Sirji framework utilizes a sophisticated logging system designed to ensure comprehensive monitoring and debugging capabilities across its components. This system is built with flexibility and scalability in mind, allowing developers to easily adjust logging levels and incorporate additional logging strategies as needed.

## Overview

Logger setup employs the Singleton and Manager design patterns to create a robust logging mechanism. This allows for consistent logging practices and easy maintenance across different parts of the Sirji framework.

### Key Components

#### LoggerSingleton

The `LoggerSingleton` class is responsible for:

- **Initialization**: Configuring individual logger instances ensuring one instance per specific purpose.
- **Custom Time Formatting**: Logging timestamps as UNIX timestamps using a custom formatter, `UnixTimestampFormatter`.
- **Dynamic Folder Management**: Creating and managing log folders based on environment variable `SIRJI_RUN_PATH`.
- **Log Level Configuration**: Setting log levels based on the `SIRJI_LOG_LEVEL` environment variable, defaulting to `debug` if not set.
- **Initialization Logs**: Providing an `initialize_logs` method to log initial messages in a simplified format.

#### LoggerManager

The `LoggerManager` class serves as a central access point for managing various logger instances within the Sirji framework. Key functionalities include:

- **Pre-configured Loggers**: Access to orchestrator and research loggers with default settings.
- **Dynamic Logger Creation**: A `create_logger` method facilitating the creation of additional loggers with specified log levels and log file path.

### Environment Variables

To configure the logging system, the following environment variables must be set:

- `SIRJI_RUN_PATH`: Specifies the run directory.
- `SIRJI_LOG_LEVEL`: Sets the log level (default is `debug`). Accepts standard logging levels (`debug`, `info`, `warning`, `error`, `critical`).

Example of setting environment variables in a Unix-like terminal:

```bash
export SIRJI_RUN_PATH=/path/to/run/directory
export SIRJI_LOG_LEVEL=info
```

### Usage

#### Accessing Pre-configured Loggers

To access the pre-configured orchestrator logger:

```python
from sirji_tools.logger import o_logger as logger
logger.info("This is an info log message for the orchestrator.")
```

To access the pre-configured research logger:

```python
from sirji_tools.logger import r_logger as logger
logger.debug("This is a debug log message for research.")
```

#### Creating and Using a Custom Logger

To create and use a custom logger:

```python
from sirji_tools.logger import create_logger
custom_logger = create_logger('custom_log_file.log', 'warning')
custom_logger.warning("This is a warning log message.")
```

### Advanced Features

- **UnixTimestampFormatter**: Custom formatter to log time as a UNIX timestamp for precise and consistent time tracking.
- **Dynamic Log File Creation**: Log files are created dynamically in directories specified in `SIRJI_RUN_PATH` environment variables inside the logs folder.
- **Log Level Configuration**: The log level can be dynamically adjusted using the `SIRJI_LOG_LEVEL` environment variable.

### Conclusion

Sirji framework's logging system is more robust, flexible, and easier to extend. The system allows for dynamic setting of log levels, management of log files and folders, and ensures accessibility and configurability of loggers across different components.
