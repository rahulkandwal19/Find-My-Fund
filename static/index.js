const slideValue = document.getElementById("sliderOutput");
const inputSlider = document.getElementById("eReturn");
inputSlider.addEventListener("change", ()=>{
    slideValue.innerHTML= "&nbsp;"+inputSlider.value + "%";
});

document.getElementById("signupButton").onclick = ()=>{
    let typeMF = document.getElementById("typeMF").value;
    let riskMF = document.getElementById("riskLevel").value;
    let eReturnMF = document.getElementById("eReturn").value;
    let MinIMF = document.getElementById("minInvestment").value;
    let MinSIPMF = document.getElementById("minSIP").value;
    let ObjMF = document.getElementById("objectiveInvestment").value;
    let data = "?type="+typeMF+"&risk="+riskMF+"&return="+eReturnMF+"&minInv="+MinIMF+"&minSIP="+MinSIPMF+"&obj="+ObjMF;

    window.location.href = ('/getMutualFunds'+data);
}
