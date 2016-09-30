var WebRtcDemo = WebRtcDemo || {};

/************************************************
ViewModel.js
 
************************************************/
WebRtcDemo.ViewModel = (function () {
    var viewModel = {
        Users: [],
        Bots: [],
        DisplayName: '', // My username, to be reflected in UI
        MyConnectionId: -1
    };

     
    

    // Return the viewmodel so that we can change props later
    return viewModel;
})();