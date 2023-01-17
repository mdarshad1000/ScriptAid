```
    let plus = document.createElement("span");
    plus.setAttribute("onclick", "addField(this)");
    plus.setAttribute("class", "buttons");
    let plusText = document.createTextNode("+");
    plus.appendChild(plusText);
```
1. let plus = document.createElement("span"); - This line creates a new span element and assigns it to the variable plus. The createElement() method is used to create a new element with the specified tag name.

2. plus.setAttribute("onclick", "addField(this)"); - This line sets an onclick attribute on the span element and assigns it the value "addField(this)". This means that when the span element is clicked, the JavaScript function addField(this) will be called.

3. plus.setAttribute("class", "buttons"); - This line sets the class attribute on the span element and assigns it the value "buttons". This class can be used to style the element.

4. let plusText = document.createTextNode("+"); - This line creates a new text node containing the "+" character and assigns it to the variable plusText

5. plus.appendChild(plusText); - This line appends the text node created on the previous line as a child of the span element using the appendChild() method. This will add the "+" character as the content of the span element.