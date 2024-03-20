# Logger Setup for Sirji Framework

The Sirji framework utilizes a sophisticated logging system designed to ensure comprehensive monitoring and debugging capabilities across its components. This system is built with flexibility and scalability in mind, allowing developers to easily adjust logging levels and incorporate additional logging strategies as needed.

## Overview

Logger setup employs the Singleton and Manager design patterns to create a robust logging mechanism. This allows for consistent logging practices and easy maintenance across different parts of the Sirji framework.

### Components

#### LoggerSingleton

The `LoggerSingleton` class is responsible for initializing and configuring individual logger instances. It ensures that each logger is a singleton, meaning that only one instance of a logger for a specific category exists throughout the application's lifecycle.

#### LoggerManager

The `LoggerManager` class acts as a central point for accessing and managing the various logger instances within the Sirji framework. It simplifies the logger retrieval process and encapsulates the logic for logger initialization.

### Setting Up Log Levels

The default log level can be adjusted by setting the `SIRJI_LOG_LEVEL` environment variable. This variable accepts standard logging level strings (`debug`, `info`, `warning`, `error`, `critical`), providing flexibility in controlling log output verbosity.

### Set log level env var:
```bash
export SIRJI_LOG_LEVEL=info
```

### Sample Usage of Logger specific to coder:
```python
from tools.logger import coder as logger
logger.info("Log line here")
```

### Sample Usage of Logger specific to researcher:
```python
from tools.logger import researcher as logger
logger.info("Log line here")
```