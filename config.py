import os
import random

class Config:
    
    MONGO_URI = os.getenv("MONGO_URI") or "mongodb+srv://a9756549615:twWV3d6JJ6ubHKUC@cluster0.bhqyt.mongodb.net/cricketinsights?retryWrites=true&w=majority&appName=Cluster0"
    SECRET_KEY = os.getenv("SECRET_KEY") or "".join(
        [chr(random.randint(65, 92)) for _ in range(50)]
    )