# tischkicker

## Prerequisites

You need Python3.11 and node.js with npm installed.

## Starting the dev server

If you installed the latest version of our `d` shortcut ([link]("https://github.com/SD-Software-Design-GmbH/Developers-Playground/tree/master/bash-scripts")), all you need is

```bash
d r
```

else, use

```
./scripts/run.sh
```

or, in two separate terminals

```
python mananage.py runserver
```

```
npm run dev
```

## Setup

1. Setup a virtual environment
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate
    ```
2. Install requirements
    ```bash
    pip install -r requirements.dev.txt
    ```
3. Install node dependencies
    ```bash
    npm i
    ```
4. Load the dev settings

    ```bash
    echo "from .base import *
    from .dev import *

    try:
        from .local import *
    except ModuleNotFoundError:
        pass
    " >> tischkicker/settings/__init__.py
    ```

## Static files in deployment

1. Static files must first be bundled by vite and can then be collected
    ```bash
    npm run build
    python manage.py collectstatic
    ```
