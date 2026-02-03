import { Schema, model, Document } from 'mongoose';
import bcrypt from 'bcryptjs';

// 用户接口
export interface IUser {
  username: string;
  email: string;
  password: string;
  createdAt?: Date;
  updatedAt?: Date;
}

// 用户文档接口
export interface IUserDocument extends IUser, Document {
  comparePassword(candidatePassword: string): Promise<boolean>;
}

// 用户 Schema
const userSchema = new Schema<IUserDocument>(
  {
    username: {
      type: String,
      required: true,
      unique: true,
      trim: true,
      minlength: 3,
      maxlength: 30,
    },
    email: {
      type: String,
      required: true,
      unique: true,
      trim: true,
      lowercase: true,
      match: [/^\S+@\S+\.\S+$/, '请输入有效的邮箱地址'],
    },
    password: {
      type: String,
      required: true,
      minlength: 6,
      select: false, // 查询时不返回密码
    },
  },
  {
    timestamps: true,
  }
);

// 用户模型
const UserModel = model<IUserDocument>('User', userSchema);

export default UserModel;
