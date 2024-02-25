To deploy this project

The commands below assumes you will deploy this project in the us-east-1 region, if you deploy this project in a different region then replace "us-east-1" with the region used.

```
git clone git@github.com:chiwaichan/feedmyfurbabies-cdk-iot-timestream.git
cd feedmyfurbabies-cdk-iot-timestream
cdk deploy

git remote rm origin
git remote add origin https://git-codecommit.us-east-1.amazonaws.com/v1/repos/feedmyfurbabies-cdk-iot-timestream-FeedMyFurBabiesCodeCommitRepo
git push --set-upstream origin main
```

Please visit [https://chiwaichan.co.nz](https://chiwaichan.co.nz) for an in-depth explanation of the architecture deployed in this project.