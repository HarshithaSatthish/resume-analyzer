const PASSWORD_MIN_LENGTH = 8;

export function validatePassword(password) {
  if (!password || password.length < PASSWORD_MIN_LENGTH) {
    return `Password must be at least ${PASSWORD_MIN_LENGTH} characters long.`;
  }
  if (!/[A-Za-z]/.test(password)) {
    return 'Password must contain at least one letter.';
  }
  if (!/\d/.test(password)) {
    return 'Password must contain at least one number.';
  }
  return null;
}

export function validatePasswordMatch(password, confirmPassword) {
  if (password !== confirmPassword) {
    return 'Passwords do not match.';
  }
  return null;
}
