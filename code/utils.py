def get_retention_actions(churn_prob):
    """Generate retention recommendations"""
    if churn_prob > 0.6:
        return [
            "🚨 **IMMEDIATE ACTION REQUIRED**",
            "📞 Call customer within 24 hours",
            "💰 Offer 25% discount + free premium",
            "🎁 Send personalized retention gift",
            "📧 Priority support escalation"
        ]
    elif churn_prob > 0.4:
        return [
            "⚠️ **PROACTIVE RETENTION**",
            "📧 Send targeted retention email", 
            "💳 Double rewards points offer",
            "📅 Schedule satisfaction call",
            "🎯 Recommend product upgrade"
        ]
    else:
        return [
            "✅ **LOW RISK**",
            "Continue normal service",
            "Monitor quarterly",
            "Standard engagement cadence"
        ]
