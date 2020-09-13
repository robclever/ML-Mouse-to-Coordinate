# ML-Mouse-to-Coordinate
 Logistic Regression model trained on moving mouse to user specified coordinate, trained on data from user.
 
## Dependencies:
- Python 3.8, required by the version of keras/tensorflow used in training
- pyautogui
- mouse
- random
- pandas
- numpy
- tensorflow
- keras
- sklearn
- pickle
- matplotlib

## General Flow:
 To start, run the _game/graphics.py_ to create training data for the neural network to train on. Once training data has been created, you can then run _training/net_train.py_ to train a network on the data. After training, the network can be tested by running the _testing/use_net_model.py_ function.
 
## Future Upgrades:
1. Script tuning_pipeline.py
- Build a tuning pipeline to automatically find net/training parameters through random search
2. MultiNet
- Implement a multiple net structure to move the mouse fast when the position error is large, and slow when the position error is small
3. API Test
- Incorporate this project with a computer vision algorithm that performs object recognition
