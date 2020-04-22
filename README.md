
## Real time sentiment analysis: Ludwig deep learning framework in action

![](sentiment_demo.gif)


### App:

http://ec2-35-171-231-143.compute-1.amazonaws.com:8050

### Data:

https://www.kaggle.com/bittlingmayer/amazonreviews

### Run the app locally:

Clone repo:
```
git clone https://github.com/dostoyevsky1/ludwig_sentiment_dash.git
```
Run from inside repo using Docker Compose:
```
docker-compose build
docker-compose up
```
App will be accessible at: http://localhost:8050

### Run on your own EC2 linux instance:

SSH into your EC2:
```
ssh -i path/to/key.pem ec2-user@public-ip-address
```
Install docker:
```
sudo yum update -y
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -a -G docker ec2-user
```
Log-out, log back in and install docker-compose:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
Test the install:
```
docker-compose --version
```
Install git and clone repo:
```
sudo yum install git
git clone https://github.com/dostoyevsky1/ludwig_sentiment_dash.git
```
Run app:
```
cd ludwig_sentiment_dash
docker-compose up --build -d
```
App will be accessible at: http://your-ec2-public-DNS:8050

------------------------
*Please fork and add functionality*

X Online learning / automatic model updating based on submitted reviews.

X Page to display table of sample rows from DB.

X Admin page + authentication
