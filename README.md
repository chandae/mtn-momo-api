# MTN MoMo API
## Production Python Module

You need production credentials (Subscription key, API User ID, API User Key). The MTN MoMo API host is https://proxy.momoapi.mtn.com. Check the various endpoints in the document at https://momoapi.mtn.com/docs/services/collection/operations/bc-authorize-POST

<br />

## Download project
Download/clone this repository with the commands below and navigate to root of the project:

> Make sure you have git installed and configured

```bash
$ # clone repository
$ git clone https://github.com/chandae/mtn-momo-dev.git
$ cd momo-api-dev
```

<br />

## Create a virtual environment
Create a virtual environment for this project. Ensure that you have the virtualenv module. Run:
```bash
$ # create virtual environment
$ virtualenv .venv
```
> .venv is the name of the virtual environment. Feel free to use a different name.

<br />

Activate the virtual environment with:
```bash
$ # activate virtual environment
$ source .venv/bin/activate
```

<br />

## Install dependencies
Check requirements.txt for a list of dependencies. Install project dependencies with the command:
> Ensure that your virtual environment is active

```bash
$ # Install dependencies within environment
$ python -m pip install -r requirements.txt
```

## Environment variables
Create a .env file in the root directory of the project. In the file, add the following variables with respective keys:
1. USERNAME
2. PASSWORD
3. SUBSCRIPTION KEY

## READY TO USE API

Example:
```python
if __name__ == "__main__":
    # use actual mtn momo number here
    payer_number = ""

    req = MomoPaymentRequest("1", payer_number, "ZMW", "test payment")
    req.send()
    time.sleep(25)
    req.payment_status()
```
