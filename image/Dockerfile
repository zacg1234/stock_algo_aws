FROM public.ecr.aws/lambda/python:3.10

# Copy requirements.txt to the root of the lambda 
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy all files from ./src folder to root of Lambda
COPY src/* ${LAMBDA_TASK_ROOT}

# Set the main handler of the function
CMD [ "main.handler" ]