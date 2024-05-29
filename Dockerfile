
FROM public.ecr.aws/lambda/python:3.10

WORKDIR ${LAMBDA_TASK_ROOT}

COPY creds_aws.py kiwi_api_key.py lambda_function.py new_full_list_with_countries.csv ./

RUN ls -al

RUN pip install pandas requests boto3

CMD ["lambda_function.lambda_handler"]