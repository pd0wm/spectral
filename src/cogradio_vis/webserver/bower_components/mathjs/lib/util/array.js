'use strict';

var number = require('./number'),
    string = require('./string'),
    object = require('./object'),
    types = require('./types'),

    DimensionError = require('../error/DimensionError'),
    IndexError = require('../error/IndexError'),

    isArray = Array.isArray;

/**
 * Calculate the size of a multi dimensional array.
 * @param {Array} x
 * @Return {Number[]} size
 * @private
 */
function _size(x) {
  var size = [];

  while (isArray(x)) {
    size.push(x.length);
    x = x[0];
  }

  return size;
}

/**
 * Calculate the size of a multi dimensional array.
 * All elements in the array are checked for matching dimensions using the
 * method validate
 * @param {Array} x
 * @Return {Number[]} size
 * @throws RangeError
 */
exports.size = function(x) {
  // calculate the size
  var s = _size(x);

  // verify the size
  exports.validate(x, s);
  // TODO: don't validate here? only in a Matrix constructor?

  return s;
};

/**
 * Recursively validate whether each element in a multi dimensional array
 * has a size corresponding to the provided size array.
 * @param {Array} array    Array to be validated
 * @param {Number[]} size  Array with the size of each dimension
 * @param {Number} dim   Current dimension
 * @throws DimensionError
 * @private
 */
function _validate(array, size, dim) {
  var i;
  var len = array.length;

  if (len != size[dim]) {
    throw new DimensionError(len, size[dim]);
  }

  if (dim < size.length - 1) {
    // recursively validate each child array
    var dimNext = dim + 1;
    for (i = 0; i < len; i++) {
      var child = array[i];
      if (!isArray(child)) {
        throw new DimensionError(size.length - 1, size.length, '<');
      }
      _validate(array[i], size, dimNext);
    }
  }
  else {
    // last dimension. none of the childs may be an array
    for (i = 0; i < len; i++) {
      if (isArray(array[i])) {
        throw new DimensionError(size.length + 1, size.length, '>');
      }
    }
  }
}

/**
 * Validate whether each element in a multi dimensional array has
 * a size corresponding to the provided size array.
 * @param {Array} array    Array to be validated
 * @param {Number[]} size  Array with the size of each dimension
 * @throws DimensionError
 */
exports.validate = function(array, size) {
  var isScalar = (size.length == 0);
  if (isScalar) {
    // scalar
    if (isArray(array)) {
      throw new DimensionError(array.length, 0);
    }
  }
  else {
    // array
    _validate(array, size, 0);
  }
};

/**
 * Test whether index is an integer number with index >= 0 and index < length
 * @param {Number} index    Zero-based index
 * @param {Number} [length] Length of the array
 */
exports.validateIndex = function(index, length) {
  if (!number.isNumber(index) || !number.isInteger(index)) {
    throw new TypeError('Index must be an integer (value: ' + index + ')');
  }
  if (index < 0) {
    throw new IndexError(index);
  }
  if (length !== undefined && index >= length) {
    throw new IndexError(index, length);
  }
};

// a constant used to specify an undefined defaultValue
exports.UNINITIALIZED = {};

/**
 * Resize a multi dimensional array. The resized array is returned.
 * @param {Array} array         Array to be resized
 * @param {Array.<Number>} size Array with the size of each dimension
 * @param {*} [defaultValue=0]  Value to be filled in in new entries,
 *                              zero by default. To leave new entries undefined,
 *                              specify array.UNINITIALIZED as defaultValue
 * @return {Array} array         The resized array
 */
exports.resize = function(array, size, defaultValue) {
  // TODO: add support for scalars, having size=[] ?

  // check the type of the arguments
  if (!isArray(array) || !isArray(size)) {
    throw new TypeError('Array expected');
  }
  if (size.length === 0) {
    throw new Error('Resizing to scalar is not supported');
  }

  // check whether size contains positive integers
  size.forEach(function (value) {
    if (!number.isNumber(value) || !number.isInteger(value) || value < 0) {
      throw new TypeError('Invalid size, must contain positive integers ' +
          '(size: ' + string.format(size) + ')');
    }
  });

  // recursively resize the array
  var _defaultValue = (defaultValue !== undefined) ? defaultValue : 0;
  _resize(array, size, 0, _defaultValue);

  return array;
};

/**
 * Recursively resize a multi dimensional array
 * @param {Array} array         Array to be resized
 * @param {Number[]} size       Array with the size of each dimension
 * @param {Number} dim          Current dimension
 * @param {*} [defaultValue]    Value to be filled in in new entries,
 *                              undefined by default.
 * @private
 */
function _resize (array, size, dim, defaultValue) {
  var i;
  var elem;
  var oldLen = array.length;
  var newLen = size[dim];
  var minLen = Math.min(oldLen, newLen);

  // apply new length
  array.length = newLen;

  if (dim < size.length - 1) {
    // non-last dimension
    var dimNext = dim + 1;

    // resize existing child arrays
    for (i = 0; i < minLen; i++) {
      // resize child array
      elem = array[i];
      if (!isArray(elem)) {
        elem = [elem]; // add a dimension
        array[i] = elem;
      }
      _resize(elem, size, dimNext, defaultValue);
    }

    // create new child arrays
    for (i = minLen; i < newLen; i++) {
      // get child array
      elem = [];
      array[i] = elem;

      // resize new child array
      _resize(elem, size, dimNext, defaultValue);
    }
  }
  else {
    // last dimension

    // remove dimensions of existing values
    for (i = 0; i < minLen; i++) {
      while (isArray(array[i])) {
        array[i] = array[i][0];
      }
    }

    if(defaultValue !== exports.UNINITIALIZED) {
      // fill new elements with the default value
      for (i = minLen; i < newLen; i++) {
        array[i] = object.clone(defaultValue);
      }
    }
  }
}

/**
 * Squeeze a multi dimensional array
 * @param {Array} array
 * @param {Array} [size]
 * @returns {Array} returns the array itself
 * @private
 */
exports.squeeze = function(array, size) {
  var s = size || exports.size(array);

  // squeeze outer dimensions
  while (isArray(array) && array.length === 1) {
    array = array[0];
    s.shift();
  }

  // find the first dimension to be squeezed
  var dims = s.length;
  while (s[dims - 1] === 1) {
    dims--;
  }

  // squeeze inner dimensions
  if (dims < s.length) {
    array = _squeeze(array, dims, 0);
    s.length = dims;
  }

  return array;
};

/**
 * Recursively squeeze a multi dimensional array
 * @param {Array} array
 * @param {number} dims Required number of dimensions
 * @param {number} dim  Current dimension
 * @returns {Array | *} Returns the squeezed array
 * @private
 */
function _squeeze (array, dims, dim) {
  var i, ii;

  if (dim < dims) {
    var next = dim + 1;
    for (i = 0, ii = array.length; i < ii; i++) {
      array[i] = _squeeze(array[i], dims, next);
    }
  }
  else {
    while (isArray(array)) {
      array = array[0];
    }
  }

  return array;
}

/**
 * Unsqueeze a multi dimensional array: add dimensions when missing
 * @param {Array} array
 * @param {Number} dims     Desired number of dimensions of the array
 * @param {Number} [outer]  Number of outer dimensions to be added
 * @param {Array} [size]    Current size of array
 * @returns {Array} returns the array itself
 * @private
 */
exports.unsqueeze = function(array, dims, outer, size) {
  var s = size || exports.size(array);

  // unsqueeze outer dimensions
  if (outer) {
    for (var i = 0; i < outer; i++) {
      array = [array];
      s.unshift(1);
    }
  }

  // unsqueeze inner dimensions
  array = _unsqueeze(array, dims, 0);
  while (s.length < dims) {
    s.push(1);
  }

  return array;
};

/**
 * Recursively unsqueeze a multi dimensional array
 * @param {Array} array
 * @param {number} dims Required number of dimensions
 * @param {number} dim  Current dimension
 * @returns {Array | *} Returns the squeezed array
 * @private
 */
function _unsqueeze (array, dims, dim) {
  var i, ii;

  if (isArray(array)) {
    var next = dim + 1;
    for (i = 0, ii = array.length; i < ii; i++) {
      array[i] = _unsqueeze(array[i], dims, next);
    }
  }
  else {
    for (var d = dim; d < dims; d++) {
      array = [array];
    }
  }

  return array;
}
/**
 * Flatten a multi dimensional array, put all elements in a one dimensional
 * array
 * @param {Array} array   A multi dimensional array
 * @return {Array}        The flattened array (1 dimensional)
 * @private
 */
exports.flatten = function(array) {
  if (!Array.isArray(array)) {
    //if not an array, return as is
    return array;
  }
  var flat = [];

  array.forEach(function callback(value) {
    if (Array.isArray(value)) {
      value.forEach(callback);  //traverse through sub-arrays recursively
    }
    else {
      flat.push(value);
    }
  });

  return flat;
};

/**
 * Convert function arguments to an array.
 * @param {Arguments} args
 * @returns {Array} array
 */
exports.argsToArray = function(args) {
  var array = [];
  for (var i = 0, len = args.length; i < len; i++) {
    array[i] = args[i];
  }
  return array;
};

/**
 * Test whether an object is an array
 * @param {*} value
 * @return {Boolean} isArray
 */
exports.isArray = isArray;
