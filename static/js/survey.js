Survey
    .StylesManager
    .applyTheme("default");

var json = {
    "completeText": "Finish",
    "pageNextText": "Continue",
    "pagePrevText": "Previous",
    "pages": [
        {
            "elements": [
                {
                    "type": "panel",
                    "elements": [
                        {
                            "type": "html",
                            "name": "tool_intro",
                            "html": "<article class='intro'>  <h1 class='intro__heading intro__heading--income title' style='color:grey'>        Spending Budget Survey        </h1>       <div class='intro__body wysiwyg'>    <p> In this section, you will be asked about your periodical spending (weekly, monthly or annually) for different items.</p>    <p>The tool will automatically group your spendings to essential and discretionary buckets and calculate your retirement goals </p>    </div>     </article>"
                        }
                    ],
                    "name": "panel1"
                }
            ],
            "name": "page0"
        },
        {
            "name": "page1",
            "elements": [
                {
                    "type":"panel",
                    "name": "essential",
                    "title": "Essential Spending",
                    "elements": [
                        {
                            "type": "paneldynamic",
                            "renderMode": "progressTop",
                            "allowAddPanel": false,
                            "allowRemovePanel": false,
                            "name": "house",
                            "title": "Housing Essentials",
                            "valueName": "house",
                            "panelCount": 1,
                            "templateElements":[

                                {
                                    "type": "panel",
                                    "name": "rent",
                                    "title": "Rent and/or mortage with property taxes",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "inputType": "number",
                                            "name": "amount_1",
                                            "title": "Spending Amount",
                                            "defaultValue":0
                                        }, {
                                            "type": "dropdown",
                                            "name": "frequency_1",
                                            "title": "Spending Frequency",
                                            "startWithNewLine": false,
                                            "defaultValue": "Monthly",
                                            "choices": ["Daily","Weekly","Monthly", "Annually"]
                                        }
                                    ]
                                },

                                {
                                    "type": "panel",
                                    "name": "utility",
                                    "title": "Utilities (water, gas, electricity, etc.)",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "inputType": "number",
                                            "name": "amount_2",
                                            "title": "Spending Amount",
                                            "defaultValue":0
                                        }, {
                                            "type": "dropdown",
                                            "name": "frequency_2",
                                            "title": "Spending Frequency",
                                            "startWithNewLine": false,
                                            "defaultValue": "Monthly",
                                            "choices": ["Daily","Weekly","Monthly", "Annually"]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "paneldynamic",
                            "renderMode": "progressTop",
                            "allowAddPanel": false,
                            "allowRemovePanel": false,
                            "name": "transportation",
                            "title": "Transportation Daily Commute Essentials",
                            "valueName": "transportation",
                            "panelCount": 1,
                            "templateElements":[

                                {
                                    "type": "panel",
                                    "name": "public",
                                    "title": "Public Transportion - Train, Bus, Taxi, Other",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "inputType": "number",
                                            "name": "amount_1",
                                            "title": "Spending Amount",
                                            "defaultValue":0
                                        }, {
                                            "type": "dropdown",
                                            "name": "frequency_1",
                                            "title": "Spending Frequency",
                                            "startWithNewLine": false,
                                            "defaultValue": "Daily",
                                            "choices": ["Daily","Weekly","Monthly", "Annually"]
                                        }
                                    ]
                                },

                                {
                                    "type": "panel",
                                    "name": "private",
                                    "title": "Private Vehicles - Depreciation/Lease and Services & Repairs",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "inputType": "number",
                                            "name": "amount_2",
                                            "title": "Spending Amount",
                                            "defaultValue":0
                                        }, {
                                            "type": "dropdown",
                                            "name": "frequency_2",
                                            "title": "Spending Frequency",
                                            "startWithNewLine": false,
                                            "defaultValue": "Annually",
                                            "choices": ["Daily","Weekly","Monthly", "Annually"]
                                        }
                                    ]
                                },

                                {
                                    "type": "panel",
                                    "name": "other",
                                    "title": "Private Vehicles - Insurance, Gas, Parking, Car Wash",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "inputType": "number",
                                            "name": "amount_3",
                                            "title": "Spending Amount",
                                            "defaultValue":0
                                        }, {
                                            "type": "dropdown",
                                            "name": "frequency_3",
                                            "title": "Spending Frequency",
                                            "startWithNewLine": false,
                                            "defaultValue": "Monthly",
                                            "choices": ["Daily","Weekly","Monthly", "Annually"]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "paneldynamic",
                            "renderMode": "progressTop",
                            "allowAddPanel": false,
                            "allowRemovePanel": false,
                            "name": "living",
                            "title": "Food and Other Basic Living Essentials",
                            "valueName": "living",
                            "panelCount": 1,
                            "templateElements":[

                                {
                                    "type": "panel",
                                    "name": "grocery",
                                    "title": "Groceries and Household supplies",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "inputType": "number",
                                            "name": "amount_1",
                                            "title": "Spending Amount",
                                            "defaultValue":0
                                        }, {
                                            "type": "dropdown",
                                            "name": "frequency_1",
                                            "title": "Spending Frequency",
                                            "startWithNewLine": false,
                                            "defaultValue": "Weekly",
                                            "choices": ["Daily","Weekly","Monthly", "Annually"]
                                        }
                                    ]
                                },

                                {
                                    "type": "panel",
                                    "name": "clothing",
                                    "title": "Clothing",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "inputType": "number",
                                            "name": "amount_2",
                                            "title": "Spending Amount",
                                            "defaultValue":0
                                        }, {
                                            "type": "dropdown",
                                            "name": "frequency_2",
                                            "title": "Spending Frequency",
                                            "startWithNewLine": false,
                                            "defaultValue": "Weekly",
                                            "choices": ["Daily","Weekly","Monthly", "Annually"]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "name": "page2",
            "elements": [
                {
                    "type":"panel",
                    "name": "freedom",
                    "title": "Freedom Spending",
                    "elements":[
                        {
                            "type": "paneldynamic",
                            "renderMode": "progressTop",
                            "allowAddPanel": false,
                            "allowRemovePanel": false,
                            "name": "entertainment",
                            "title": "Entertainment",
                            "valueName": "entertainment",
                            "panelCount": 1,
                            "templateElements":[

                                {
                                    "type": "panel",
                                    "name": "restaurant",
                                    "title": "Restaurants & Drinks",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "inputType": "number",
                                            "name": "amount_1",
                                            "title": "Spending Amount",
                                            "defaultValue":0
                                        }, {
                                            "type": "dropdown",
                                            "name": "frequency_1",
                                            "title": "Spending Frequency",
                                            "startWithNewLine": false,
                                            "defaultValue": "Monthly",
                                            "choices": ["Daily","Weekly","Monthly", "Annually"]
                                        }
                                    ]
                                },

                                {
                                    "type": "panel",
                                    "name": "event",
                                    "title": "Events (sports, music, theather etc.)",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "inputType": "number",
                                            "name": "amount_2",
                                            "title": "Spending Amount",
                                            "defaultValue":0
                                        }, {
                                            "type": "dropdown",
                                            "name": "frequency_2",
                                            "title": "Spending Frequency",
                                            "startWithNewLine": false,
                                            "defaultValue": "Monthly",
                                            "choices": ["Daily","Weekly","Monthly", "Annually"]
                                        }
                                    ]
                                }
                            ]
                        }

                    ]
                }
            ]
        }
    ]
};


var modal = document.getElementById("survey");

$("#open-survey").on('click',function(event){

    modal.style.display = "block";

    window.survey = new Survey.Model(json);

    survey
        .onComplete
        .add(function (result) {
            // document
            //     .querySelector('#surveyResult')
            //     .textContent = "Result JSON:\n" + JSON.stringify(result.data, null, 3);
            console.log(result.data);
        });


    $("#surveyElement").Survey({model: survey});;

    window.onclick = function(event) {
        if (event.target == modal) {
          modal.style.display = "none";
        }
    };
    
});


