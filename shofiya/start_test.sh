export FLASK_ENV = Testing

pytest --cov-report html --cov=blueprint tests/
export FLASK_ENV = Development

# sh start_test.sh