import Redis from 'ioredis';

// Redis配置接口
export interface IRedisConfig {
  host: string;
  port: number;
  password?: string;
  db?: number;
}

// Redis客户端类
class RedisClient {
  private client: Redis;

  constructor(config: IRedisConfig) {
    this.client = new Redis({
      host: config.host,
      port: config.port,
      password: config.password,
      db: config.db || 0,
    });
  }

  // 获取Redis客户端
  public getClient(): Redis {
    return this.client;
  }

  // 设置限流数据
  public async setRateLimit(key: string, count: number, window: number): Promise<void> {
    await this.client.setex(key, window, count.toString());
  }

  // 获取限流数据
  public async getRateLimit(key: string): Promise<number | null> {
    const data = await this.client.get(key);
    return data ? parseInt(data, 10) : null;
  }

  // 删除限流数据
  public async delRateLimit(key: string): Promise<void> {
    await this.client.del(key);
  }

  // 关闭连接
  public async close(): Promise<void> {
    await this.client.quit();
  }
}

// 创建Redis客户端实例
const redisConfig: IRedisConfig = {
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
  password: process.env.REDIS_PASSWORD,
  db: parseInt(process.env.REDIS_DB || '0'),
};

export const redisClient = new RedisClient(redisConfig);
export default redisClient;
