$km_prices = @(15, 13, 19)
$dockerhub_namespace = "nickolaus899"
$base_image_name = "logistic-api"
$python_version = "3.12-slim"

foreach ($i in 0..2) {
    $id = $i + 1
    $km_price = $km_prices[$i]
    
    $dockerfile_content = @"
FROM python:$python_version
WORKDIR /app

COPY data/ data
COPY src/ src

COPY .env .
COPY requirements.txt .
COPY main.py .

RUN pip install --no-cache-dir -r requirements.txt

ENV KM_PRICE=$km_price
ENV CONTAINER_ID=$id

CMD ["python", "main.py", "$id", "$km_price"]
"@
    $dockerfile_path = "Dockerfile$id"
    Set-Content -Path $dockerfile_path -Value $dockerfile_content

    $tag = "${dockerhub_namespace}/${base_image_name}-v${id}:latest"
    docker build -f $dockerfile_path -t $tag .

    docker push $tag
}

Write-Host "`nAll operations completed successfully!"