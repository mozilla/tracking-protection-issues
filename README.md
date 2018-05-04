# webcompat-blipz-experiment-issues

Private repo used to host the code for filing issues from the webcompat-blipz-experiement web extension, *and* as a place to collect those private issues.

## Local installation

We're using [pipenv](https://docs.pipenv.org/) for this project. Be sure to [install it first](https://docs.pipenv.org/#install-pipenv-today).

0. clone the repo
1. `pipenv sync --dev`
2. `pipenv run flask run`

Note: If you're trying to use this in production, it will expect a `OAUTH_TOKEN` environment variable, which contains a valid GitHub Oauth personal token.

🚨 Please don't ever add it to the `.env` file and check it in. 🚨