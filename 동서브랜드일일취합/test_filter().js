const numbers = [1,2,3,4,5];
const result = numbers.filter(number => number > 3);

console.log(numbers);
console.log(result);


numbers.filter((num, index, source) => {

  console.log(num);
  console.log()
})