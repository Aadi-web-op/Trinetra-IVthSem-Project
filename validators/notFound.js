const notFound = (req, res, next) => {
  res.status(404);
  throw new Error(`Not Found - ${req.originalUrl}`);
};

module.exports = notFound;