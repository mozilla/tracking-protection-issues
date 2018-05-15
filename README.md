# webcompat-blipz-experiment-issues

[![CircleCI](https://circleci.com/gh/mozilla/webcompat-blipz-experiment-issues.svg?style=svg&circle-token=85b98f657531c7f90e84082cd9220d1babf27fd6)](https://circleci.com/gh/mozilla/webcompat-blipz-experiment-issues)

Repo used to host the code for filing issues from the webcompat-blipz-experiement web extension. Actual user-reported issues are not filed here, but elsewhere.

## Local installation

We're using [pipenv](https://docs.pipenv.org/) for this project. Be sure to [install it first](https://docs.pipenv.org/#install-pipenv-today).

0. clone the repo
1. `pipenv sync --dev`
2. `pipenv run flask run`

Note: If you're trying to use this in production, it will expect a lot of environment variables. Check out config.py.

🚨 Please don't ever add any to the `.env` file and check it in. 🚨

## How it works

This server exposes a `/new` endpoint that expects the following `multipart/form-data` payload via `POST`, represented here in some kind of pseudo-schema:

{
  "body": the issue body (required)
  "title": the issue title (required),
  "screenshot": base64 encoded jpeg (optional),
  "labels": array of strings (optional)
}

A GitHub issue will be created, assuming all the credentials are correct, and if there's a screenshot in the payload, it will be uploaded to a private s3 bucket. Once that is done, a link to the uploaded image will be posted as a comment in the newly created issue. For privacy and security reasons, the GitHub repo and its issues are private and locked down to a small team of Mozilla employees within the @mozilla GitHub org. If you think you need access, ping miket@mozilla.com. The s3 bucket is restricted to people with IAM access, and the images are not accessible from GitHub issues.
