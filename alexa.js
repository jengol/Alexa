var https=require('https')
exports.handler = (event,context) => {
    try{
if(event.session.new){
    //New Session when the new skill starts
console.log("NEW SESSION")
}
switch(event.request.type){
    case "LaunchRequest":
    // > Launch Request if you invoke the skill with just the invocation name just said "Emotion Articles"
    console.log('LAUNCH REQUEST')
    context.succeed(
        generateResponse(
            buildSpeechletResponse("Welcome to an Alexa Skill, this is running on a deployed lambda function", true),
            {}
        )
    )
    break;

    case"IntentRequest":
    // > Intent Request if you invoke the skill with the intent name like "Emotion Article, Get Happy"
console.log('INTENT REQUEST')

switch(event.request.intent.name)
{
    case "GetHappy":
    context.succeed(
        generateResponse(
            buildSpeechletResponse('I am happy that you are happy.', true),
            {}
        )
    )
break;

case "GetSad":
context.succeed(
    generateResponse(
        buildSpeechletResponse('I am sad that you are sad.', true),
        {}
)
    )
break;
       
default:
throw "Invalid intent"
}
break;

case "SessionEndedRequest":
    // > Session Ended Request exiting the skill
    console.log('SESSION ENDED REQUEST')
    break;

    default:
    context.fail('INVALID REQUEST TYPE: ${event.request.type}')
}
}
    
    catch(error){ context.fail('Exception: ${error}')}
}
//Helpesr
buildSpeechletResponse=(outputText, shouldEndSession) => {
    return {
        outputSpeech:
        {
            type:"PlainText",
            text: outputText
        },
        shouldEndSession: shouldEndSession
    }
}

generateResponse= (speechletResponse, sessionAttributes) => {
    return {
        version: "1.0",
        sessionAttributes: sessionAttributes,
        response: speechletResponse
    }
}
