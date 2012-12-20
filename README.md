tt-chart-service
================

## Configuration

    heroku config:set TT_CHART_SERVICE_TOKEN=<secret>


## Local Testing

    python tests.py


## Live Testing

    curl --data "svg=`cat test.svg`" $web_url/render/?token=$TT_CHART_SERVICE_TOKEN


## License

Apache 2.0
