const User = require("../models/userModel");
const bcrypt = require("bcryptjs");

exports.createUser = async (data) => {
  const hashedPassword = await bcrypt.hash(data.password, 10);

  return await User.create({
    ...data,
    password: hashedPassword,
  });
};