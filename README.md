# Tracking Protection Issues

TODO: add circle-ci

Repo used to host the code for filing private tracking protection issues. 

## Local installation

We're using [pipenv](https://docs.pipenv.org/) for this project. Be sure to [install it first](https://docs.pipenv.org/#install-pipenv-today).

0. clone the repo
1. `pipenv sync --dev`
2. `pipenv run flask run`

Note: If you're trying to use this in production, it will expect a lot of environment variables. Check out config.py.

🚨 Please don't ever add any to the `.env` file and check it in. 🚨

## How it works

This server exposes a `/new` endpoint that expects the following `multipart/form-data` payload via `POST`, represented here in some kind of pseudo-schema:

```
{
  "body": the issue body (required)
  "title": the issue title (required),
  "labels": array of strings (optional)
}
```

A GitHub issue will be created, assuming all the credentials are correct. 

For privacy and security reasons, the GitHub repo and its issues are private and locked down to a small team of Mozilla employees within the @mozilla GitHub org. If you think you need access, ping miket@mozilla.com.
