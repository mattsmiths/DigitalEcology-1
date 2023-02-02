# basicR.R
# Written by James Crall
# Intro for ENTOM 375: Digital Ecology, S' 2023

# This is a comment! Lines with a '#' at the beginning are not interpreted as code, and can be used to add notes/descriptions
# NB this is true in both R and Python


### basic variables and manipulation
x <- 5 
  # The '<-' symbol assigns the value on the right the variable on the right - equivalent to '5 -> x'
  #Notice also that now the 'Environment' window in the upper right has a new variable, 'x', with value 5

print(x) #Prints to the Console window. 
#This is an example of a function ('print') with an input ('x')
#Each function will have different kinds of inputs

y <- 10
  #Define a second variable
z  = x + y

print(z)


### Vectors
v1 <- c(2,6,9)
  #This line uses the 'concatenate' function ('c') to combine three numbers into a single variable, which is a vector

v2 <- c(4,7,10)
  #Create a second vector of the same length

plot(v1, v2)
  #Plot these two vectors against each other
  #Note that 

# Reach: Try modifying these vectors with unique numbers, and extending to 5 numbers each

#Operations on vector
v1_squared <- v1^2
  #This creates another vector of equal length 

#Sequences
x <- 1:10
print(x)
  #This generates a vector with integers from 1 to 10
  #Reach: check out the 'seq' function and read about it with '?seq' in the console, and try to generate a vector of 100 

#Indexing vectors
print(v1[2]) #This prints the second item in 

#Generating random number vectors
v1 <-runif(10) #This create a vector with ten random numbers (between 0 and 1).
  #Note that this overwrote the 'v1' variable above

# Now make a similar vector, but adding on a sequence of integers from 1 to 10
# This will make a set of increasing numbers with random noise added
v1 <- runif(10) + 1:10

v2 <- runif(10) + 1:10
  #Create a second vector of the same length

plot(v1,v2)
  #Now plot these against each other



### Data frames
  #Data frames are relative flexible formats that can hold multiple vectors and data types, sort of like a spreadsheet within R
my_data <- data.frame('Var_1' = v1, 'Var_2' = v2)

#Indexing from data frames
print(my_data[,1])
print(my_data$Var_1)
  #Notice that these give the same output!



### Libraries (this adds a unique set of functions).
  #If this line gives you an error, make sure 'ggplot2' is intalled in the 'Packages' window, if not install
library(ggplot2)

#Alternative plotting with ggplot
ggplot(my_data, aes(x = Var_1, y = Var_2))+geom_point()
