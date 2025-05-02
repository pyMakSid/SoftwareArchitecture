## Лабораторная работа №5: Cache

1. Для данных, хранящихся в реляционной базе PotgreSQL реализуйте шаблон сквозное чтение и сквозная запись (Пользователь/Клиент …);
2. В качестве кеша – используйте Redis
3. Замерьте производительность запросов на чтение данных с и без кеша с использованием утилиты wrk https://github.com/wg/wrk изменяя количество потоков из которых производятся запросы (1, 5, 10)
4. Актуализируйте модель архитектуры в Structurizr DSL
5. Ваши сервисы должны запускаться через docker-compose командой docker- compose up (создайте Docker файлы для каждого сервиса)


## Results:

### 1 threads and 10 connections
No redis:
```
Running 10s test @ http://127.0.0.1:8000
  1 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.25ms  200.65us   9.96ms   82.79%
    Req/Sec     8.06k   213.07     8.35k    92.08%
  81027 requests in 10.10s, 11.90MB read
  Non-2xx or 3xx responses: 81027
Requests/sec:   8022.82
Transfer/sec:      1.18MB
```
Redis:
```
Running 10s test @ http://127.0.0.1:8000
  1 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.18ms  168.97us   7.14ms   72.53%
    Req/Sec     8.52k   198.42     9.09k    81.19%
  85606 requests in 10.10s, 12.57MB read
  Non-2xx or 3xx responses: 85606
Requests/sec:   8476.07
Transfer/sec:      1.24MB
```
### 5 threads and 10 connections
No redis:
```
Running 10s test @ http://127.0.0.1:8000
  5 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.23ms  189.54us   8.83ms   79.80%
    Req/Sec     1.63k   146.07     3.86k    98.61%
  81540 requests in 10.10s, 11.98MB read
  Non-2xx or 3xx responses: 81540
Requests/sec:   8073.92
Transfer/sec:      1.19MB
```
Redis:
```
Running 10s test @ http://127.0.0.1:8000
5 threads and 10 connections
Thread Stats   Avg      Stdev     Max   +/- Stdev
  Latency     1.17ms  182.13us   7.54ms   73.97%
  Req/Sec     1.71k    85.43     2.64k    95.43%
85818 requests in 10.10s, 12.60MB read
Non-2xx or 3xx responses: 85818
Requests/sec:   8496.80
Transfer/sec:      1.25MB
```
### 10 threads and 10 connections
No redis:
```
Running 10s test @ http://127.0.0.1:8000
  10 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.25ms  192.60us   8.94ms   80.19%
    Req/Sec   805.40     23.79     0.85k    85.60%
  80192 requests in 10.01s, 11.78MB read
  Non-2xx or 3xx responses: 80192
Requests/sec:   8014.18
Transfer/sec:      1.18MB
```
Redis:
```
Running 10s test @ http://127.0.0.1:8000
  10 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.18ms  187.27us   8.63ms   78.41%
    Req/Sec   847.71     26.39     0.99k    80.60%
  84429 requests in 10.01s, 12.40MB read
  Non-2xx or 3xx responses: 84429
Requests/sec:   8436.66
Transfer/sec:      1.24MB
```
