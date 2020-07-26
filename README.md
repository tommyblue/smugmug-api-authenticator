# SmugMug API OAuth 1 authenticator

This is a very simple web application that can help you to obtain the user tokens required to
use SmugMug API and the [SmugMug Backup App](https://github.com/tommyblue/smugmug-backup).

A live version exists at [https://smugmug-api-authenticator.herokuapp.com/](https://smugmug-api-authenticator.herokuapp.com/), feel free to use it if you trust me. But if you don't (and you should not trust anyone in
the wild), then clone this repository and run the app by yourself.

To run the app locally:

```bash
git clone https://github.com/tommyblue/smugmug-api-authenticator.git
cd smugmug-api-authenticator
# Optional: create and activate a python 3 virtualenv
pip install -r requirements.txt
./run_dev_server.sh
```
