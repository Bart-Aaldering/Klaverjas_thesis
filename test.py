
from AlphaZero.alphazero import AlphaZero_train
from AlphaZero.networks import create_normal_nn

def main():
    mcts_params = {
        "mcts_steps": 10,
        "n_of_sims": 1,
        "nn_scaler": 0.5,
        "ucb_c": 50,
    }
    # model = create_normal_nn()
    model = None
    train = AlphaZero_train().selfplay(mcts_params, model, 5)

if __name__ == "__main__":
    main()
    # import time
    # e = set([1,2,3,4,5,6,7,8,9,10])
    # b = set([1,2,3,9,10])
    # t = time.time()
    # d = True
    # for i in range(1000000):
    #     a = {i for i in range(10)}
    #     if d:
    #         e |= a
    #     b -= a
    #     # for i in range(10):
    #     #     if d:
    #     #         e.add
    #     #     b.discard(i)
    # # print(a)
    # print(time.time() - t)  
