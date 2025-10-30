from time import monotonic, sleep

def timer():
    start = monotonic()

    def inner(message):
        print(f'{message}: {monotonic() - start:.2f}')

    return inner

if __name__ == '__main__':
    t = timer()
    t('hello world')
    t('hello world 1')
    sleep(3)
    t('hello world 2')
    sleep(2)
    t('hello world 3')
