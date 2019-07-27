Survey
    .StylesManager
    .applyTheme("default");

var json = {
    "completeText": "Finish",
    "pageNextText": "Continue",
    "pagePrevText": "Previous"
};


var page0 = {
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
};

var essential_spending_list = 
[
    {
        "name": "house",
        "title": "Housing Essentials",
        "bucket_list": [
            {
                "name": "rent",
                "title": "Rent and/or mortage with property taxes",
                "default_fre": "Monthly"
            },
            {
                "name": "utility",
                "title": "Utilities (water, gas, electricity, etc.)",
                "default_fre": "Monthly"
            }
        ]
    },
    {
        "name": "transportation",
        "title": "Transportation Daily Commute Essentials",
        "bucket_list": [
            {
                "name": "public",
                "title": "Public Transportion - Train, Bus, Taxi, Other",
                "default_fre": "Daily"
            },
            {
                "name": "private",
                "title": "Private Vehicles - Depreciation/Lease and Services & Repairs",
                "default_fre": "Annually"
            }
        ]
    },
    {
        "name": "digital",
        "title": "Digital Services Essentials",
        "bucket_list": [
            {
                "name": "basic",
                "title": "Internet, Phone, TV",
                "default_fre": "Monthly"
            },
            {
                "name": "other",
                "title": "Other Subscriptions",
                "default_fre": "Monthly"
            }
        ]
    },
    {
        "name": "living",
        "title": "Food and Other Basic Living Essentials",
        "bucket_list": [
            {
                "name": "grocery",
                "title": "Groceries and Household supplies",
                "default_fre": "Monthly"
            },
            {
                "name": "clothing",
                "title": "Clothing",
                "default_fre": "Monthly"
            },
            {
                "name": "other",
                "title": "Other",
                "default_fre": "Monthly"
            }
        ]
    },
    {
        "name": "health",
        "title": "Health Essential Expenditures & Provisions",
        "bucket_list": [
            {
                "name": "standard",
                "title": "Out-of-pocket standard healthcare costs (insurance, medications, etc.)",
                "default_fre": "Monthly"
            },
            {
                "name": "additional",
                "title": "Additional out-of-pocket non-standard costs (e.g., long-term care, surgery)",
                "default_fre": "Monthly"
            }
        ]
    }
];

var freedom_spending_list = 
[
    {
        "name": "entertainment",
        "title": "Entertainment",
        "bucket_list": [
            {
                "name": "restaurant",
                "title": "Restaurants & Drinks",
                "default_fre": "Monthly"
            },
            {
                "name": "event",
                "title": "Events (sports, music, theather etc.)",
                "default_fre": "Monthly"
            }
        ]
    },
    {
        "name": "Shopping",
        "title": "Shopping",
        "bucket_list": [
            {
                "name": "electronics",
                "title": "Electronics and home goods (computer, phone, appliances)",
                "default_fre": "Annually"
            },
            {
                "name": "luxury",
                "title": "Luxury Items (clothes, jewellery)",
                "default_fre": "Monthly"
            }
        ]
    },
    {
        "name": "Vacation",
        "title": "Vacation and non-standard Travel",
        "bucket_list": [
            {
                "name": "Flights",
                "title": "Flights",
                "default_fre": "Monthly"
            },
            {
                "name": "Lodge",
                "title": "Lodging: hotels, airbnb, etc",
                "default_fre": "Monthly"
            }
        ]
    }
];

const mapToElementLower = function(bucket) {

    return {
        "type": "panel",
        "name": bucket["name"],
        "title": bucket["title"],
        "elements": [
            {
                "type": "text",
                "inputType": "number",
                "name": "amount_"+bucket["name"],
                "title": "Spending Amount",
                "defaultValue":0
            }, {
                "type": "dropdown",
                "name": "frequency_"+bucket["name"],
                "title": "Spending Frequency",
                "startWithNewLine": false,
                "defaultValue": bucket["default_fre"],
                "choices": ["Daily","Weekly","Monthly", "Annually"]
            }
        ]
    };
};

const mapToElementHigher = function(panel) {

    var bucket_element_list = panel["bucket_list"].map(d => mapToElementLower(d));

    return panel_element = {
        "type": "paneldynamic",
        "renderMode": "progressTop",
        "allowAddPanel": false,
        "allowRemovePanel": false,
        "name": panel["name"],
        "title": panel["title"],
        "panelCount": 1,    
        "templateElements":bucket_element_list
    };
        
};

var page1 = {
    "name": "page1",
    "elements": [
        {
            "type":"panel",
            "name": "essential",
            "title": "Essential Spending",
            "elements":essential_spending_list.map(d => mapToElementHigher(d))
        }
    ]
};

var page2 = {
    "name": "page1",
    "elements": [
        {
            "type":"panel",
            "name": "essential",
            "title": "Essential Spending",
            "elements":freedom_spending_list.map(d => mapToElementHigher(d))
        }
    ]
};


var pages = [page0,page1,page2];

json["pages"] = pages;

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


