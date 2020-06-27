
if __name__ == "__main__":
    from rabbitmq.process import start_consumer
    import sys
    import os
    cd = os.getcwd()
    target = sys.argv[1]
    start_consumer(target)


