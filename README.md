# Chat analytic

Analyze your chat history, then show basic statistics and some visualized graphs

## Scripts

```shell
# update requirements.txt file
pip3 freeze > requirements.txt

# install package from requirements.txt file
pip3 install -r ./requirements.txt

# activate virtualenv
source ./venv/bin/activate

# run app
uvicorn app.main:app --reload

# login to gcloud
gcloud auth login

# switch gclound account
gcloud config set account mala.ut.29@gmail.com

# deploy app to google app engine
gcloud app deploy app.yaml --project maximal-furnace-371714
```

## References

1. <https://www.analyticsvidhya.com/blog/2021/04/whatsapp-group-chat-analyzer-using-python>

## Notes

1. deta.sh not suport MongoDB and have so many limitations <https://docs.deta.sh/docs/micros/about/#important-notes>
