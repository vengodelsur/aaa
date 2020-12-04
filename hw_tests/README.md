`pip install -r requirements.txt`

`coverage erase`

`coverage run --source . -m pytest --doctest-modules -vv *.py > result`

`coverage html`